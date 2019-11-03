<!DOCTYPE html>
<html lang="en">

<head>
    <title>Post-queries to yandex-messenger backend</title>
    <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
    <meta charset="utf-8">
    <style>
        body {
            background-color: #eee;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: space-around;
            align-items: flex-start;
            font-family: sans-serif;
        }
        body > div {
            padding: 10px 30px;
            margin: 20px 30px;
            background-color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 2px solid gray;
            border-radius: 20px;
        }
        body > div > form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        input {
            border: 1px solid gray;
            border-radius: 10px;
            padding: 5px;
            font-size: 120%;
        }
        button {
            padding: 10px 40px;
            margin-top: 20px;
            border: 1px solid gray;
            border-radius: 10px;
            font-size: 120%;
            background-color: #eee;
        }
    </style>
</head>

<body>

    <div>
        <h1>register_user.php</h1>
        <form target="_blank" action=register_user.php method=post>
            <p>name : </p>
            <input name="name">

            <p>handle : </p>
            <input name="handle">

            <p>email : </p>
            <input name="email">

            <p>password : </p>
            <input name="password">

            <button type=submit>Send</button>
        </form>
    </div>

    <div>
        <h1>login.php</h1>
        <form target="_blank" action=login.php method=post>
            <p>handle : </p>
            <input name="handle">

            <p>password : </p>
            <input name="password" type="password">

            <button type=submit>Send</button>
        </form>
    </div>

    <div>
        <h1>check_handle.php</h1>
        <form target="_blank" action=check_handle.php method=post>
            <p>handle : </p>
            <input name="handle">

            <button type=submit>Send</button>
        </form>
    </div>

    <div>
        <h1>send_message.php</h1>
        <form target="_blank" action=send_message.php method=post>
            <p>from_handle : </p>
            <input name="from_handle">

            <p>token : </p>
            <input name="token">

            <p>to_handle : </p>
            <input name="to_handle">

            <p>text : </p>
            <input name="text">

            <button type=submit>Send</button>
        </form>
    </div>

    <div>
        <h1>get_messages.php</h1>
        <form target="_blank" action=get_messages.php method=post>
            <p>handle : </p>
            <input name="handle">

            <p>token : </p>
            <input name="token">

            <p>to_handle : </p>
            <input name="to_handle">

            <button type=submit>Send</button>
        </form>
    </div>

    <div>
        <h1>get_message_list.php</h1>
        <form target="_blank" action=get_message_list.php method=post>
            <p>handle : </p>
            <input name="handle">

            <p>token : </p>
            <input name="token">

            <button type=submit>Send</button>
        </form>
    </div>

</body>

</html>