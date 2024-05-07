# password-vault
Password vault to store your passwords hashed in an sqlite3 db.

## About
This project uses md5 hashing to encrypt passwords. Front end uses python tkinter and backend uses sqlite3 to store the information.

![Image](https://private-user-images.githubusercontent.com/163078067/327832605-4655d829-7c36-4d70-9904-209b0850b46d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTUxMTU2ODIsIm5iZiI6MTcxNTExNTM4MiwicGF0aCI6Ii8xNjMwNzgwNjcvMzI3ODMyNjA1LTQ2NTVkODI5LTdjMzYtNGQ3MC05OTA0LTIwOWIwODUwYjQ2ZC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNTA3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDUwN1QyMDU2MjJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xZjc4ZDIzODE4ZjUzYTEyZWE3Njg3MjI0ZTFhZjJiNWE2ZDNlOTljOTBhZDg2OGZiYzdmNGM3ZjIzMGQzZWZkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.cSoepQlW59XEdxtEXZbyyhaKSRAvweqUAysL9sfczEI)

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
