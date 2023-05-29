# URL Grabber

This script is a simple tool for grabbing and parsing HTML content from a given URL. It utilizes the `requests` library for making HTTP requests, `BeautifulSoup` for parsing HTML, and `PySimpleGUI` for creating a graphical user interface.

![image](https://github.com/AbstractEndeavors/URL_GRABBER/assets/57512254/833e4413-7f71-4a19-9716-a4609f279784)


## Features

- Enter a URL and grab its HTML content
- View and manipulate the parsed HTML using different parsing options provided by BeautifulSoup
- Customize the User-Agent header for the HTTP request
- Choose from a list of supported ciphers for the SSL/TLS connection

## Installation

To use the URL Grabber script, follow these steps:

1. Install the required Python packages by running the following command:

   ```
   pip install requests beautifulsoup4 PySimpleGUI
   ```

2. Download the script file (`url_grabber.py`) and place it in your desired directory.

3. Run the script using the following command:

   ```
   python url_grabber.py
   ```

## Usage

Upon running the script, a graphical user interface (GUI) window will appear. The window contains several input fields and buttons to interact with the script's functionality.

### URL Input

Enter the desired URL in the "URL Input" field. You can either include the protocol (e.g., `https://`) or leave it out. If the protocol is omitted, the script will automatically prepend `https://`.

Click the "Grab URL" button to fetch the HTML content from the specified URL. The parsed HTML will be displayed in the "Source Code" section below.

### Source Code

The "Source Code" section displays the fetched HTML content. You can manually edit the source code if needed.

### Parsing Options

Choose the parsing option from the "Parsing Capabilities" dropdown menu. This determines how the HTML content will be parsed using BeautifulSoup.

- **BeautifulSoup**: The main BeautifulSoup class used for parsing HTML.
- **Tag**: Represents an HTML tag.
- **NavigableString**: Represents a string within an HTML document.
- **Comment**: Represents an HTML comment.
- **ResultSet**: Represents a collection of tags found during a search.
- **SoupStrainer**: Allows parsing only a specific subset of the HTML document.
- **CData**: Represents a CDATA section within an XML document.

### Find Soup

The "Find Soup" section allows you to search for specific elements within the parsed HTML. Choose the element type (tag, element, type, or class) and check the corresponding checkbox. Click the "Find Soup" button to find the matching elements in the HTML content.

### User-Agent

By default, the User-Agent header is set to a standard browser user agent. You can customize the User-Agent header by enabling the "Custom User-Agent" checkbox and selecting a user agent from the dropdown menu.

### SSL/TLS Ciphers

The script provides a list of supported SSL/TLS ciphers. You can customize the ciphers used for the SSL/TLS connection by enabling/disabling the checkboxes. The selected ciphers will be displayed in the "Ciphers" field.

## Contact

For any inquiries or partnership opportunities, please contact **partners@abstractendeavors.com**.

## Author

This script is developed and maintained by **putkoff** from **Abstract Endeavors**.

## GitHub Repository

The script is available on GitHub at [**abstract_endeavors/url-grabber**](https://github.com/abstract_endeavors/url-grabber).
