# News With Django
---
News With Django is a Django project of a news portal to practice with the new Django version.

* Pages

    ```Home```
    ```Details```
    ```Admin```
    
* Features

    ```Filters by category, tags and date range```    
    ```Custom admin with filters, search and so on```
    ```News content with html editor, images upload and embeds```

# Getting Started
---
## Prerequisites

* Python 3.4 or newer
* Django 2.0.6

## Usage Steps
* Fork and clone the repo

* Required modules
    
    ```pip install -r requirements.txt```

* Database
  
    ```Install the MySQL```
    ```Configure DATABASES in settings.py```
    ```python manage.py check```
    ```python manage.py migrate```
    ```python manage.py createsuperuser```

* Run the app

    ```python manage.py runserver```

* Open Your browser at

    ```localhost:8000```

## Admin

The site admin can be accessed with /no-idea
for security reasons this page is only accessible manually with this url

# HTML Article

To write the content of articles with HTML was used the [Summernote](https://github.com/summernote/django-summernote), to view and edit the source code click on "Code View" button.

For more security has been integrated with [lxml](https://lxml.de) into the admin to [sanitize](https://lxml.de/api/lxml.html.clean.Cleaner-class.html) malicious scripts,
this may prevent the use of certain codes considered unsafe, configure the white list of lxml in the admin.py if it seems appropriate.

In templates folder the file article_default_content.html is used to default structure of the articles content, you can change it completely to whatever you think is appropriate or even leave blank.

# License
This project is under MIT License 
![license](https://img.shields.io/github/license/mashape/apistatus.svg)

