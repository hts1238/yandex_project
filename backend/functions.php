<?php

function connect() {
    $DB_HOST = "s14.webhost1.ru:3306";
    $DB_LOGIN = "u216556_1";
    $DB_PASSWORD = "123456";
    $DB_NAME = "u216556_1";

    $db = mysqli_connect(
        $DB_HOST,
        $DB_LOGIN,
        $DB_PASSWORD,
        $DB_NAME
    );

    mysqli_set_charset($db, 'utf8');
    return $db;
}

function get_id_from_handle(&$db, &$handle, &$query_answer) {
    $sql = "SELECT id FROM users WHERE handle = '$handle'";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = [
            "id" => "2",
            "title" => "database error",
            "description" => mysqli_error($db)
        ];
        return false;
    }

    $sql_result =  mysqli_fetch_assoc($sql_result);

    if (!isset($sql_result["id"])) {
        $query_answer["Error"] = "Incorrect handle!";
        $query_answer["Dodo"] = $sql_result;
        return false;
    }

    return $sql_result["id"];
}

function check_user(&$db, &$user_id, &$token, &$query_answer) {
    $sql = "SELECT token_time, user_id ".
        "FROM connects ".
        "WHERE token = '$token'";
    $sql_result = mysqli_query($db, $sql);

    // If sql query was unsuccessful
    if (!$sql_result) {
        $query_answer["Error"] = [
            "id" => "2",
            "title" => "database error",
            "description" => mysqli_error($db)
        ];
        return false;
    }

    $result = mysqli_fetch_assoc($sql_result);

    // if user id is incorrect
    if ($result["user_id"] != $user_id) {
        $query_answer["Error"] = "Incorrect user id";
        return false;
    }

    // If token is older then 1 week
    if (time() - $result["token_time"] > 604800) {
        $query_answer["Error"] = "The token is old";
        return false;
    }
    else {
        $sql = "UPDATE connects ".
            "SET token_time = ".time()." ".
            "WHERE token = '$token'";
        $sql_result = mysqli_query($db, $sql);

        if (!$sql_result) {
            $query_answer["Error"] = [
                "id" => "2",
                "title" => "database error",
                "description" => mysqli_error($db)
            ];
            return false;
        }
    }
    return true;
}

function validate_data(&$name, &$handle, &$email, &$password) {
    return true;
}

function create_token() {
    $size = 25;
    $symbols = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ];
    $length = count($symbols);
    $token = '';
    for ($i = 0; $i < $size; $i++) {
        $token .= $symbols[rand(0, $length - 1)];
    }
    return $token;
}
