# BudoRent - Construction Equipment Rental Application

### My Details
- **Name**: Patryk Chamera
- **GitHub Username**: [xhamera1](https://github.com/xhamera1)
- **edX Username**: xhamera
- **City and Country**: Kraków or Stalowa Wola, Poland
- **Date of Video Recording**: 09-08-2024

### Video Demo
[Click here to view the video demo](https://youtu.be/1OVRI0UpEWo?si=pCm9kshIPI7TyBLD)

---

## Description

**BudoRent** is a mobile-responsive web application designed to streamline the rental process for construction equipment. Users can browse a variety of tools, reserve them for pickup, manage their rental history, and interact with the service through a user-friendly interface. The app is intended for individuals and companies that need temporary access to tools such as drills, screwdrivers, and ladders, without the necessity of purchasing them.

The app was built using **Flask (Python)** as the backend framework, **HTML/CSS** for the frontend, and **SQL** to handle data storage. It is designed to be simple and intuitive, enabling easy navigation and functionality for both desktop and mobile users.

---

## Key Features

### 1. **User Authentication**
Users can create an account with a secure registration system and log in to manage their profile and rentals. The authentication system ensures that user data, such as rental history and personal information, is stored securely.

### 2. **Equipment Catalog**
The application features an extensive catalog of construction equipment, allowing users to browse tools available for rent. Each tool has a dedicated page with details such as availability, price, rental terms, and a short description.

### 3. **Reservation System**
Once users find the equipment they need, they can add it to their **Cart** and proceed to reserve it. The system allows users to specify the rental duration and choose a pickup date. All reservations are stored in the database, and users receive confirmation of their bookings.

### 4. **User Account Management**
After logging in, users can access their **Profile** page, where they can:
- View and update their personal information.
- Review their **Rental History**, which shows a list of all past and current reservations.
- Manage reservations, such as canceling or modifying an upcoming rental.

### 5. **Cart**
The **Cart** allows users to store the equipment they plan to rent temporarily. Users can adjust the quantity of tools or remove items before proceeding to the reservation process. The cart provides an overview of all selected items, including pricing and estimated total costs for the rental.

### 6. **Contact Page**
The **Contact** page allows users to reach out for support or inquiries. They can fill out a contact form to ask questions about the service or report any issues. The page also displays company contact details, including phone numbers and email addresses for customer support.

---

## How the Application Works

1. **User Flow**: 
   - A user starts by registering or logging in to their account.
   - After logging in, they are redirected to the **Catalog**, where they can browse the available tools.
   - The user adds equipment to the **Cart**, adjusts the rental details, and then reserves the items.
   - After completing the reservation, the user can view it on their **Profile** page under **Rental History**.

2. **Reservation System**:
   - When a user makes a reservation, the system checks the availability of the tools based on the selected dates.
   - The reservation details are stored in the SQL database, ensuring that the inventory is updated in real-time.

3. **Profile and History**:
   - The **Profile** page allows users to view their current and past reservations. They can cancel or modify upcoming rentals depending on the store's policies.
   - All rental transactions are securely logged in the SQL database, allowing users to keep track of their rental history for future reference.

4. **Contact Page**:
   - If a user has any questions or encounters an issue, they can visit the **Contact** page, where they can fill out a form to get in touch with the service team.
   - The page also displays general contact information, such as the support email and phone number.

---

## Technologies Used

- **Flask (Python)**: The application uses Flask as the backend framework to manage routes, handle user authentication, and interface with the SQL database.
- **HTML/CSS**: Frontend languages were used to design a clean, mobile-responsive user interface, ensuring that the application is easy to use on any device.
- **SQL**: A SQL database stores all necessary data, including user profiles, equipment details, reservations, and rental history.
- **Mobile-Responsive Design**: Ensures that the application provides an optimal user experience, whether accessed on a mobile device or desktop.

---

## Conclusion

The **BudoRent** application offers a convenient platform for users to rent construction equipment without the need to purchase expensive tools. From user authentication to equipment management and rental history tracking, the project demonstrates my skills in web development, database management, and mobile-responsive design. This solution is ideal for both individuals and businesses looking to rent tools on a short-term basis.
