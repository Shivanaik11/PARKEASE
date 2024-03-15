import cv2
import pytesseract
import re
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import random
import pyrebase
import json
import qrcode
from PIL import Image, ImageTk
pytesseract.pytesseract.tesseract_cmd = r'YOUR_TESSERACT_PATH'

config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "databaseURL": "YOUR_DATABASE_URL",
    "storageBucket": "YOUR_STORAGE_BUCKET"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class ParkingSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("PARKEASE")
        self.master.configure(bg="black")
        self.entry_button = tk.Button(master, text="Entry", command=self.entry_interface, height=3, width=10, bg="green", fg="white", font=('Helvetica', 12, 'bold'))
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_interface, height=3, width=10, bg="red", fg="white", font=('Helvetica', 12, 'bold'))
        self.center_window()  
        self.master.state('zoomed')
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.entry_button.grid(row=1, column=0, padx=10, pady=(30, 10), sticky='nsew')
        self.exit_button.grid(row=1, column=1, padx=10, pady=(30, 10), sticky='nsew')
        self.load_data()
        self.entry_listener = db.child("Entry_Interface").child("status").stream(self.entry_status_change)
        self.exit_listener = db.child("Exit_Interface").child("status").stream(self.exit_status_change)

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - self.master.winfo_reqwidth()) / 2
        y_position = (screen_height - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x_position, y_position))

    def entry_status_change(self, message):
        status = message["data"]
        if status == "ENTRY_DETECTED":
            self.entry_interface()

    def exit_status_change(self, message):
        status = message["data"]
        if status == "EXIT_DETECTED":
            self.exit_interface()

    def entry_interface(self):
        EntryInterface(self.master, self, self.update_exit_display)

    def exit_interface(self):
        ExitInterface(self.master, self)

    def update_exit_display(self):
        if hasattr(self, 'exit_interface'):
            self.exit_interface.update_display()
            self.save_data()

    def load_data(self):
        try:
            data = db.child("parking_data").get().val()
            if data:
                self.parked_vehicles = data.get('parked_vehicles', {})
                self.available_parking_slots = set(data.get('available_parking_slots', range(1, 6)))
            else:
                self.parked_vehicles = {}
                self.available_parking_slots = set(range(1, 6))
        except Exception as e:
            print("Error loading data:", str(e))

    def save_data(self):
        data_to_save = {
            'entry_logs': self.get_entry_logs(),
            'exit_logs': self.get_exit_logs(),
            'available_parking_slots': list(self.available_parking_slots)
        }
        try:
            data_to_save_json = json.dumps(data_to_save, default=str)
            db.child("parking_data").update(json.loads(data_to_save_json))
            print("Data saved successfully.")
        except Exception as e:
            print("Error saving data:", str(e))

    def get_entry_logs(self):
        return {
            vehicle: {
                'entry_time': info['entry_time'],
                'parking_slot': info['parking_slot']
            }
            for vehicle, info in self.parked_vehicles.items()
        }

    def get_exit_logs(self):
        exit_logs = db.child("parking_data").child("exit_logs").get().val() or {}
        return exit_logs

    def record_exit(self, vehicle_number, entry_time, exit_time, parking_slot, total_cost):
        exit_data = {
            "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            "parking_slot": parking_slot,
            "total_cost": total_cost
        }
        try:
            db.child("parking_data").child("exit_logs").child(vehicle_number).set(exit_data)
            print(f"Exit record for {vehicle_number} saved successfully.")
        except Exception as e:
            print("Error recording exit data:", str(e))
            return
        if vehicle_number in self.parked_vehicles:
            del self.parked_vehicles[vehicle_number]
        self.available_parking_slots.add(parking_slot)
        self.save_data()

    def park_vehicle(self, vehicle_number, entry_time, parking_slot):
        if vehicle_number not in self.parked_vehicles:
            user_data = self.fetch_user_data(vehicle_number)
            if user_data:
                full_name = user_data.get("Name")
                wallet_balance = user_data.get("Wallet_Balance")
                minimum_balance = 5  # Define the minimum wallet balance required for entry
                if wallet_balance >= minimum_balance:
                    entry_data = {
                        'entry_time': entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                        'parking_slot': parking_slot,
                        'Name': full_name,
                        'wallet_balance': wallet_balance
                    }
                    self.parked_vehicles[vehicle_number] = entry_data
                    self.available_parking_slots.remove(parking_slot)
                    entry_log_ref = db.child("parking_data").child("entry_logs").child(vehicle_number)
                    entry_log_ref.set(entry_data)
                    messagebox.showinfo("Success", f"Welcome {full_name}, Park {vehicle_number} at Slot {parking_slot}")
                else:
                    messagebox.showwarning("Insufficient Funds", f"Insufficient wallet balance\n Minimum balance required: Rs.{minimum_balance}\n Add Money to your wallet and please try again!!")
            else:
                entry_data = {
                    'entry_time': entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'parking_slot': parking_slot,
                    'Name': "Guest",
                    'wallet_balance': "N/A"
                }
                self.parked_vehicles[vehicle_number] = entry_data
                self.available_parking_slots.remove(parking_slot)
                entry_log_ref = db.child("parking_data").child("entry_logs").child(vehicle_number)
                entry_log_ref.set(entry_data)
                messagebox.showinfo("Success", f"Welcome Guest, Park {vehicle_number} at Slot {parking_slot}")
        else:
            messagebox.showwarning("Warning", f"Vehicle {vehicle_number} is already parked.")
        self.save_data()

    def fetch_user_data(self, vehicle_number):
        try:
            query = db.child("users").order_by_child("Registered_Vehicle_Number").equal_to(vehicle_number).get()
            for user in query.each():
                user_data = user.val()
                print("User Data Retrieved:", user_data)
                return user.val()  
        except Exception as e:
            print("Error fetching user data:", str(e))
            return None

    def remove_vehicle(self, vehicle_number):
        if vehicle_number in self.parked_vehicles:
            parking_slot = self.parked_vehicles[vehicle_number]["parking_slot"]
            self.available_parking_slots.add(parking_slot)
            del self.parked_vehicles[vehicle_number]
            self.update_exit_display()
            messagebox.showinfo("Success", f"Vehicle {vehicle_number} exited from Slot {parking_slot}")
            self.save_data()

class EntryInterface(tk.Toplevel):
    def __init__(self, master, parking_system, exit_callback):
        super().__init__(master)
        self.title("Detected Number plate")
        self.parking_system = parking_system
        self.exit_callback = exit_callback
        recognized_plate = detect_and_extract_number_plate()
        recognized_plate = recognized_plate.replace(" ", "")
        self.vehicle_number_entry = tk.Entry(self)
        self.vehicle_number_entry.insert(tk.END, recognized_plate)
        self.vehicle_number_entry.grid(row=0, column=0, padx=10, pady=10)
        self.park_vehicle()

    def park_vehicle(self):
        if not self.validate_input():
            return
        vehicle_number = self.vehicle_number_entry.get()
        if vehicle_number in self.parking_system.parked_vehicles:
            messagebox.showwarning("Warning", f"Vehicle {vehicle_number} is already parked.")
        else:
            if not self.parking_system.available_parking_slots:
                messagebox.showwarning("Warning", "No available parking slots.")
                return
            parking_slot = random.choice(list(self.parking_system.available_parking_slots))
            entry_time = datetime.now()
            self.parking_system.park_vehicle(vehicle_number, entry_time, parking_slot)
            self.destroy()

    def validate_input(self, allow_empty=False):
        vehicle_number = self.vehicle_number_entry.get().strip().upper()
        if not allow_empty and not vehicle_number:
            messagebox.showwarning("Warning", "Please enter the vehicle number.")
            return False
        pattern = re.compile(r'^[A-Za-z]{2}\s?\d{2}\s?[A-Za-z]{1,2}\s?\d{4}$')
        if not pattern.match(vehicle_number):
            messagebox.showwarning("Warning", "Invalid vehicle number format.")
            return False
        return True

class ExitInterface(tk.Toplevel):
    def __init__(self, master, parking_system):
        super().__init__(master)
        self.title("Parking Exit System")
        self.parking_system = parking_system
        self.vehicle_number_label = tk.Label(self, text="Vehicle Number:")
        self.vehicle_number_entry = tk.Entry(self)
        self.parked_vehicles_label = tk.Label(self, text="Parked Vehicles:")
        self.parked_vehicles_text = tk.Text(self, height=10, width=30, state=tk.DISABLED)
        recognized_plate = detect_and_extract_number_plate()
        recognized_plate = recognized_plate.replace(" ", "")
        self.vehicle_number_entry.insert(tk.END, recognized_plate)
        self.vehicle_number_label.grid(row=0, column=0, padx=10, pady=10)
        self.vehicle_number_entry.grid(row=0, column=1, padx=10, pady=10)
        self.parked_vehicles_label.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
        self.parked_vehicles_text.grid(row=2, column=0, padx=10, pady=10, columnspan=3)
        self.print_receipt()

    def print_receipt(self):
        if not self.validate_input():
            return
        vehicle_number = self.vehicle_number_entry.get()
        entry_info = db.child("parking_data").child("entry_logs").child(vehicle_number).get().val()
        if entry_info:
            try:
                entry_time = datetime.strptime(entry_info["entry_time"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                entry_time = datetime.strptime(entry_info["entry_time"], "%Y-%m-%d %H:%M:%S.%f")
            parking_slot = entry_info["parking_slot"]
            exit_time = datetime.now()
            duration = exit_time - entry_time
            total_hours = duration.total_seconds() / 3600
            parking_rate = 20  # Cost per hour
            total_cost = total_hours * parking_rate
            user_data = self.parking_system.fetch_user_data(vehicle_number)
            if user_data:
                wallet_balance = float(user_data.get("Wallet_Balance", 0))
                discount = 0
                if wallet_balance >= total_cost:
                    discount = total_cost * 0.02  # 2% discount for wallet payment
                    total_cost -= discount
                    wallet_balance -= total_cost
                    
                    receipt = f"Receipt for Vehicle {vehicle_number}\n"
                    receipt += f"Parked at Slot {parking_slot} since {entry_time}\n"
                    receipt += f"Exit Time: {exit_time}\n"
                    receipt += f"Duration: {total_hours:.2f} hours\n"
                    receipt += f"Parking Cost: Rs.{total_hours * parking_rate:.2f}\n"
                    if discount > 0:
                        receipt += f"Discount@2%: Rs.{discount:.2f}\n"
                    receipt += f"Total: Rs.{total_cost:.2f}\n"
                    receipt += f"Updated Wallet Balance: Rs.{wallet_balance:.2f}"
                    print(receipt)
                    messagebox.showinfo("Billing Information", receipt)
                    self.parking_system.available_parking_slots.add(parking_slot)
                    del self.parking_system.parked_vehicles[vehicle_number]
                    self.vehicle_number_entry.delete(0, tk.END)
                    self.update_display()
                    self.parking_system.save_data()
                else:
                    messagebox.showwarning("Insufficient Funds", "Your wallet balance is insufficient to cover the parking cost\n Add Money to your wallet and please try again!!.")
            else:
                self.generate_qr_code(total_cost)
                total_cost = total_hours * parking_rate
                receipt = f"Receipt for Vehicle {vehicle_number}\n"
                receipt += f"Parked at Slot {parking_slot} since {entry_time}\n"
                receipt += f"Exit Time: {exit_time}\n"
                receipt += f"Duration: {total_hours:.2f} hours\n"
                receipt += f"Total Cost: Rs.{total_cost:.2f}"
                print(receipt)
                messagebox.showinfo("Billing Information", receipt)
                del self.parking_system.parked_vehicles[vehicle_number]
                self.parking_system.available_parking_slots.add(parking_slot)
                self.vehicle_number_entry.delete(0, tk.END)
                self.update_display()
                self.parking_system.save_data()
        else:
            messagebox.showwarning("Warning", f"Vehicle {vehicle_number} is not currently parked.")

    def generate_qr_code(self, amount):
        amount_str = "{:.1f}".format(amount)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        upi_payment_url = f"upi://pay?pa=YOUR_UPI_ID&pn=Your%20Name&am={amount_str}&cu=INR"
        qr.add_data(upi_payment_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image_tk = ImageTk.PhotoImage(qr_image)
        qr_window = tk.Toplevel(self)
        qr_window.title("QR Code for Payment")
        qr_label = tk.Label(qr_window, image=qr_image_tk)
        qr_label.pack(padx=10, pady=10)
        qr_label.image = qr_image_tk  

    def validate_input(self):
        return True

    def update_display(self):
        pass

    def update_display(self):
        self.parked_vehicles_text.config(state=tk.NORMAL)
        self.parked_vehicles_text.delete(1.0, tk.END)
        if self.parking_system.parked_vehicles:
            for vehicle, info in self.parking_system.parked_vehicles.items():
                self.parked_vehicles_text.insert(tk.END,
                                                 f"Vehicle {vehicle} parked at Slot {info['parking_slot']} since {info['entry_time']}\n")
        else:
            self.parked_vehicles_text.insert(tk.END, "No vehicles currently parked.")
        self.parked_vehicles_text.config(state=tk.DISABLED)

    def validate_input(self):
        vehicle_number = self.vehicle_number_entry.get().strip().upper()
        if not vehicle_number:
            messagebox.showwarning("Warning", "Please enter the vehicle number.")
            return False
        pattern = re.compile(r'^[A-Za-z]{2}\s?\d{2}\s?[A-Za-z]{1,2}\s?\d{4}$')
        if not pattern.match(vehicle_number):
            messagebox.showwarning("Warning", "Invalid vehicle number format.")
            return False
        return True

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(blurred, 30, 200)
    return edges

def find_contours(image):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    filtered_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)[:10]
    return filtered_contours

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, config='--oem 3 --psm 7')
    pattern = re.compile(r'^[A-Za-z]{2}\s?\d{2}\s?[A-Za-z]{1,2}\s?\d{4}$')
    match = pattern.search(text)
    filtered_text = match.group() if match else ''
    filtered_text = filtered_text.replace(" ", "")
    return filtered_text.strip()

def save_and_extract_text(image):
    cv2.imwrite('number_plate_image.jpg', image)
    saved_image = cv2.imread('number_plate_image.jpg')
    saved_image_text = extract_text_from_image(saved_image)
    print("Filtered Text from saved image:", saved_image_text)
    return saved_image_text

def detect_and_extract_number_plate():
    cap = cv2.VideoCapture(0)
    result_found = False
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    webcam_x_position = (screen_width - 640) // 2  
    webcam_y_position = (screen_height - 480) // 2
    cv2.namedWindow("Webcam")
    cv2.moveWindow("Webcam", webcam_x_position, webcam_y_position)
    while not result_found:
        ret, frame = cap.read()
        processed_frame = preprocess_image(frame)
        contours = find_contours(processed_frame)
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if 2.0 < aspect_ratio < 6.0:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    roi = frame[y:y + h, x:x + w]
                    result = save_and_extract_text(roi)
                    if result:
                        result_found = True
                        break

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return result

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingSystem(root)
    root.mainloop()
