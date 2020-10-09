# ChatroomCLI
Basic Chatroom where multiple users can send and receive messages at the same time. This application was developed with Python 3.8.4.

## Setup

### Install Requirements
```
pip install -r requirements.txt
```

### Initilize Virtual Environment
```
python -m venv venv
```

### Source Virtual Environment
Windows
```
.\venv\Scripts\activate.bat
```

Linux
```
source venv/bin/activate
```

## Usage
Start Server
```
python server.py
```

Start Client and select you unique username
```shell
python client.py [username]
```
Now you can type and send messages by hitting return.


## Stored values
Open the database. This will create the database file if it does not exist.
```
sqlite3 my_db.db
```
For the installation refer to the [sqlite homepage](https://www.sqlite.org/index.html).  
If the file was created you have to create the table:
```
sqlite> create table message (timestamp text not null, username text not null, content text not null);
```
Visualize all messages:
```
sqlite> select * from message;
```
See how many messages were sent:
```
sqlite> select count(username) from message;
```

## How it looks like
![Chatroom Example][chatroom]

![Datbase Example][db]

[chatroom]: https://github.com/CanIALugRoamOn/ChatroomCLI/tree/main/test/chatroom.png "Chatroom Example"
[db]: https://github.com/CanIALugRoamOn/ChatroomCLI/tree/main/test/db.png "Database Example"
