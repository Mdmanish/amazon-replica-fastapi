# FastAPI Amazon Clone

This is a clone of Amazon built using FastAPI, a modern, fast (high-performance), web framework for building APIs.

## Overview

This project aims to replicate the core functionalities of Amazon, providing users with a familiar shopping experience. It utilizes FastAPI on the backend to handle API requests and React.js on the frontend for the user interface.

## Features

- **User Authentication**: Allow users to sign up, log in, and manage their accounts securely.
- **Product Listings**: Display a variety of products categorized into different departments.
- **Shopping Cart**: Enable users to add/remove items to/from their cart and proceed to checkout.
- **Order Management**: Allow users to view and manage their orders.
- **Search Functionality**: Implement search functionality to easily find products.

## Technologies Used

- **Backend**:
  - FastAPI
  - SQLAlchemy (for database operations)
  - JWT (for user authentication)

- **Frontend**:
  - React.js
  - Redux (for state management)
  - Axios (for HTTP requests)

- **Database**:
  - SQLite (for development)

## Getting Started

To run this project locally, follow these steps:

1. Clone this repository to your local machine.

2. Navigate to the project directory.

3. Install dependencies for the backend:

   cd ../backend

   pip install -r requirements.txt
   
4. Run the backend server:
    ```
    uvicorn app.main:app --reload
    ```
5. Access the API's
    ```
    http://127.0.0.1:8000/docs/
    ```
