# password-vault
Password vault to store your passwords hashed in an sqlite3 db.

## About
This project uses md5 hashing to encrypt passwords. Front end uses python tkinter and backend uses sqlite3 to store the information.

## Running the Program

### Creating Your Own Vault
Copy the password-vault.py file to your computer and rename the vault to whatever you would like.
```python
window.title("Nick's Password Vault")
```

On your first time opening the program, you will be prompted to create a "Master" password. After your first time you will login using this password. To reset your password, you can remove the .db file and delete all the associated passwords to bring you to the original master password creation screen.

### Adding an Entry
Click the "Add Entry" button at the top of the screen and enter all the information in the popup.

### Removing an Entry
Click the "Delete Entry" button at the end of the desired entry.

### Filtering by Category
You can use the Category button in the top left hand corner of the screen to filter which category's entries you want to look at.

## Creds
Inspiration and many techniques drawn from [RaxoCoding](https://www.youtube.com/watch?v=UrH2WCoYEVo).
