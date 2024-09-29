import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon

class WebEnginePage(QWebEnginePage):
    """Custom QWebEnginePage to handle full-screen requests."""
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        return True

class Monsearch(QMainWindow):
    def __init__(self):
        super(Monsearch, self).__init__()

        # Set the window title and size
        self.setWindowTitle("Monsearch Web Browser")
        self.setGeometry(300, 150, 1200, 800)

        # Set the window icon
        self.setWindowIcon(QIcon("monsearch_icon.png"))

        # Create a central widget with tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)  # Allow moving tabs
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        # Add the tabs widget to the main window
        self.setCentralWidget(self.tabs)

        # Create the navigation bar
        self.create_nav_bar()

        # Create the first tab
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def create_nav_bar(self):
        """Create the navigation toolbar."""
        self.nav_bar = QToolBar("Navigation")
        self.nav_bar.setIconSize(QSize(24, 24))
        self.update_nav_bar_style()

        self.addToolBar(self.nav_bar)

        # Back button
        back_button = QAction("⟵", self)
        back_button.triggered.connect(self.go_back)
        self.nav_bar.addAction(back_button)

        # Forward button
        forward_button = QAction("⟶", self)
        forward_button.triggered.connect(self.go_forward)
        self.nav_bar.addAction(forward_button)

        # Reload button
        reload_button = QAction("⟳", self)
        reload_button.triggered.connect(self.reload_page)
        self.nav_bar.addAction(reload_button)

        # Home button
        home_button = QAction("🏠", self)
        home_button.triggered.connect(self.navigate_home)
        self.nav_bar.addAction(home_button)

        # Theme toggle button
        theme_button = QAction("🎨 Change Theme", self)
        theme_button.triggered.connect(self.change_theme)
        self.nav_bar.addAction(theme_button)

        # Settings button
        settings_button = QAction("⚙️", self)
        settings_button.triggered.connect(self.open_settings)
        self.nav_bar.addAction(settings_button)

        # Signup button
        signup_button = QAction("📝 Sign Up", self)
        signup_button.triggered.connect(self.open_signup)
        self.nav_bar.addAction(signup_button)

        # Add space between the buttons and the URL bar
        self.nav_bar.addSeparator()

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        # Add new tab button to toolbar
        new_tab_button = QAction("+", self)
        new_tab_button.triggered.connect(self.add_blank_tab)
        self.nav_bar.addAction(new_tab_button)

    def update_nav_bar_style(self):
        """Update the style of the navigation bar."""
        self.nav_bar.setStyleSheet("""
            QToolBar { background-color: #444; padding: 5px; border: 2px solid red; }
            QToolButton { background-color: #555; color: white; border-radius: 5px; padding: 5px; }
            QToolButton:hover { background-color: #777; }
            QLineEdit { background-color: #222; color: white; border: none; padding: 5px; border-radius: 5px; font-size: 14px; width: 400px; }
        """)

    def add_new_tab(self, qurl=None, label="New Tab"):
        """Add a new tab with a web view."""
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        # Create a new web view
        browser = QWebEngineView()
        page = WebEnginePage()
        browser.setPage(page)

        # Handle full-screen requests
        browser.page().fullScreenRequested.connect(self.handle_full_screen_request)

        # Enable context menu for inspection
        browser.setContextMenuPolicy(Qt.CustomContextMenu)
        browser.customContextMenuRequested.connect(self.show_context_menu)

        browser.setUrl(qurl)

        # Add the tab
        self.tabs.addTab(browser, label)
        self.tabs.setCurrentWidget(browser)  # Set the current tab to the new one

        # Connect URL changes to update the URL bar
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))

    def show_context_menu(self, pos):
        """Show the context menu for inspection."""
        menu = QMenu()
        inspect_action = QAction("Inspect", self)
        inspect_action.triggered.connect(self.inspect_element)
        menu.addAction(inspect_action)
        menu.exec_(self.current_tab().mapToGlobal(pos))

    def inspect_element(self):
        """Inspect the current page."""
        self.current_tab().page().runJavaScript("console.log('Inspecting...')")

    def change_theme(self):
        """Change the theme of the toolbar."""
        # Example theme change; toggle between dark and light
        current_style = self.nav_bar.styleSheet()
        if "background-color: #444" in current_style:
            self.nav_bar.setStyleSheet("""
                QToolBar { background-color: #fff; padding: 5px; border: 2px solid red; }
                QToolButton { background-color: #eee; color: black; border-radius: 5px; padding: 5px; }
                QToolButton:hover { background-color: #ddd; }
                QLineEdit { background-color: #fff; color: black; border: none; padding: 5px; border-radius: 5px; font-size: 14px; width: 400px; }
            """)
        else:
            self.update_nav_bar_style()

    def add_blank_tab(self):
        """Add a blank new tab."""
        self.add_new_tab(QUrl("https://www.google.com"), "New Tab")

    def close_tab(self, i):
        """Close the tab at index i."""
        if self.tabs.count() < 2:
            return  # Don't close the last tab
        self.tabs.removeTab(i)

    def go_back(self):
        """Navigate back in the current tab."""
        self.current_tab().back()

    def go_forward(self):
        """Navigate forward in the current tab."""
        self.current_tab().forward()

    def reload_page(self):
        """Reload the current tab."""
        self.current_tab().reload()

    def navigate_home(self):
        """Navigate to the home page (Google)."""
        self.current_tab().setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        """Navigate to the URL typed in the URL bar."""
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current_tab().setUrl(QUrl(url))

    def current_tab(self):
        """Return the current active web view."""
        return self.tabs.currentWidget()

    def update_url(self, q, browser=None):
        """Update the URL bar to match the current tab."""
        if browser == self.current_tab():
            self.url_bar.setText(q.toString())

    def update_url_bar(self):
        """Update the URL bar when switching tabs."""
        browser = self.current_tab()
        if browser:
            self.url_bar.setText(browser.url().toString())

    def handle_full_screen_request(self, request):
        """Handle full-screen requests from web content."""
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()
        request.accept()

    def open_settings(self):
        """Open the settings dialog."""
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings are under construction."))
        settings_dialog.setLayout(layout)
        
        settings_dialog.exec_()

    def open_signup(self):
        """Open the signup dialog."""
        signup_dialog = QDialog(self)
        signup_dialog.setWindowTitle("Sign Up")
        signup_dialog.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Create your Mon account:"))
        
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        signup_dialog.setLayout(layout)
        
        signup_dialog.exec_()

    def signup(self):
        """Handle signup logic."""
        username = self.username_input.text()
        password = self.password_input.text()
        # Here you would typically save the username and password
        print(f"User signed up: {username}")

# Main method to run the browser
if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Monsearch Browser")

    # Create and show the main window
    window = Monsearch()
    window.show()

    sys.exit(app.exec_())
