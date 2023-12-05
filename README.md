**MVCC System with Flask and Python**
=====================================

**Project Description**
-----------------------

This project implements a basic Multi-Version Concurrency Control (MVCC) system using Python, Flask, and Pickle. It's designed to demonstrate the principles of MVCC in a simple client-server architecture. The Flask application acts as the server managing data operations and ensuring concurrency control, while the Python script functions as the client, allowing user interaction with the server.

**Features**
------------

-   Start, write, commit, and rollback transactions.
-   Read committed data.
-   Concurrency control with threading locks.
-   Simple data persistence using Pickle.

**Getting Started**
-------------------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### **Prerequisites**

-   Python 3
-   Flask
-   requests (Python package)

You can install Flask and requests using pip:

```
pip install Flask requests
```

### **Installation**

Clone the GitHub repository:

```
git clone https://github.com/codewithhritik/273-mvcc.git
cd 273-mvcc
```

### **Running the Server**

Navigate to the server directory and run the Flask application:

```
cd server
python server.py
```

### **Running the Client**

Open a new terminal window and navigate to the client directory:

```
cd client
python client.py
```

**Usage**
---------

The client script provides a command-line interface to interact with the server. You can perform the following operations:

-   **`start`**: Start a new transaction.
-   **`write`**: Write data in the format of key-value pairs.
-   **`read`**: Read data by key.
-   **`commit`**: Commit the current transaction.
-   **`rollback`**: Rollback the current transaction.
-   **`exit`**: Exit the client application.

**Architecture**
----------------

The system is built on a client-server model. The Flask server handles data operations and concurrency control, while the client script allows users to send requests to the server. Data is stored in-memory and persisted using a Pickle file.

### **Server**

The Flask server provides several endpoints for transaction management (**`/start`**, **`/write`**, **`/read`**, **`/commit`**, **`/rollback`**). It uses a threading lock to manage concurrent access to shared data.

### **Client**

The Python client script interacts with the server through a simple command-line interface, sending HTTP requests to perform MVCC operations.