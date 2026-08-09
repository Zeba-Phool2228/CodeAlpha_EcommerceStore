# CodeAlpha_EcommerceStore

A professional E-commerce Store developed using Django, HTML, CSS, JavaScript, and SQLite as part of the **CodeAlpha Full Stack Development Internship**.

The project provides a complete online shopping experience with user authentication, product browsing, search and filtering, shopping cart management, checkout, order management, user profile, and contact pages.

---

## 📌 Project Overview

**CodeAlpha_EcommerceStore** is a Django-based E-commerce web application designed to demonstrate practical Full Stack Development skills.

The application provides a clean and responsive shopping interface where users can browse products, view product details, add products to their cart, place orders, and manage their orders.

The project also includes user authentication, category-based product browsing, search and sorting functionality, and dedicated profile and contact pages.

---

## ✨ Features

### 👤 User Authentication

- User Registration / Sign Up
- User Login
- User Logout
- Authentication-protected shopping and order features

### 🛍️ Product Management

- Product listing
- Product detail pages
- Product images
- Product descriptions
- Product pricing
- Stock availability
- Featured products
- Category-based browsing

### 🔎 Search & Sorting

- Search products by:
  - Product name
  - Description
  - Category
  - Brand
  - SKU
- Sort products by:
  - Price: Low to High
  - Price: High to Low
  - Name: A to Z
  - Name: Z to A
  - Newest Products

### 🛒 Shopping Cart

- Add products to cart
- Increase product quantity
- Decrease product quantity
- Remove products from cart
- Automatic cart quantity handling
- Stock-aware quantity control

### 💳 Checkout & Orders

- Checkout form
- Order creation
- Order items and quantities
- Order total calculation
- Order confirmation page
- Order history
- Order details page
- Order status tracking
- Order cancellation when applicable

### 👤 My Profile

- Username
- Email
- Membership date
- Total orders
- Quick access to My Orders

### 📞 Contact Page

- Store contact information
- Email
- Phone
- Location

### 🎨 UI / UX

- Responsive Bootstrap-based design
- Professional navigation bar
- Product cards
- Category cards
- Featured product section
- Responsive layouts
- Bootstrap Icons
- Poppins typography
- Custom CSS styling
- Clean and consistent user interface

---

## 🛠️ Technologies Used

### Python
**Purpose:** Backend programming and application logic.

### Django
**Purpose:** Web framework used to build the backend, routing, authentication, database interaction, and e-commerce functionality.

### HTML5
**Purpose:** Structure and content of the web pages.

### CSS3
**Purpose:** Custom styling, layouts, spacing, colors, and responsive design.

### JavaScript
**Purpose:** Client-side functionality and interactive behavior.

### Bootstrap 5
**Purpose:** Responsive layouts, navigation, buttons, cards, forms, and UI components.

### Bootstrap Icons
**Purpose:** Icons used throughout the navigation bar, product sections, profile, contact, cart, and other interface elements.

### Poppins
**Purpose:** Modern typography used throughout the website interface.

### SQLite
**Purpose:** Database used for storing users, products, categories, carts, orders, and related application data.

### Git & GitHub
**Purpose:** Version control and source-code repository management.

---

## 📂 Project Structure

```text
CodeAlpha_EcommerceStore/
│
├── backend/
│
├── docs/
│   ├── screenshots/
│   │   ├── All Products
│   │   ├── Cart Page
│   │   ├── Categories
│   │   ├── Category Computer - Accessories
│   │   ├── Category Home-Kitchen Products
│   │   ├── Category Sports
│   │   ├── Checkout Page
│   │   ├── Featured
│   │   ├── Homepage
│   │   ├── My Orders
│   │   ├── Order Details Page
│   │   ├── Contact us Page
│   │   └── My Profile Page
│   │
│   └── demo/
│       └── Website working video
│
├── media/
├── static/
├── store/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .gitignore
└── README.md