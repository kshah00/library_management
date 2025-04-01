# Library Management System

A comprehensive Django-based library management system that helps librarians and users manage books, magazines, borrowings, and memberships efficiently.

## Features

- **Book Management**
  - Add, edit, and delete books
  - Track book availability
  - Search books by title, author, or ISBN
  - Filter books by category
  - Upload book cover images

- **Magazine Management**
  - Manage magazine collections
  - Track magazine availability
  - Search and filter magazines

- **Member Management**
  - Register and manage library members
  - Track member borrowing history
  - Manage member status

- **Borrowing System**
  - Issue books and magazines to members
  - Track due dates and returns
  - Handle overdue items
  - Generate borrowing reports

- **Advanced Features**
  - Custom exception handling
  - Form validation with regex
  - Responsive design
  - User authentication
  - Admin interface

## Technical Details

- Built with Django 5.1.7
- Uses Bootstrap 5 for responsive design
- Implements OOP concepts with abstract base classes
- Custom exception handling
- Regular expression validation
- Database integration with SQLite
- File upload handling for cover images

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library-management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

```
library_management/
├── library/                 # Main app directory
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin interface
│   └── exceptions.py       # Custom exceptions
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── library/           # App-specific templates
├── static/                # Static files
│   ├── css/              # CSS files
│   └── js/               # JavaScript files
├── media/                 # User-uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Project dependencies
```

## Usage

1. **Admin Interface**
   - Access at `/admin/`
   - Manage books, magazines, members, and borrowings
   - View and edit all records

2. **Public Interface**
   - Browse books and magazines
   - Search and filter items
   - View item details

3. **Member Features**
   - View borrowing history
   - Check due dates
   - Request items

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django documentation
- Bootstrap team
- Font Awesome icons 