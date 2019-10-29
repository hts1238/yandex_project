<?php
/*
 *  This script send SQL query to database from the machine describing by token and user id
 *  This script require 3 post-arguments: "user_id", "token" and "sql_query"
 */

header('Content-Type: application/json');

include_once("functions.php");

function makequery(&$query_answer) {
    if (!isset($_POST["user_id"]) || !isset($_POST["token"]) || !isset($_POST["sql_query"]) ) {
        $query_answer["Error"] = "There's no any wanted arguments";
        return;
    }

    $user_id = $_POST["user_id"];
    $token = $_POST["token"];
    $sql_query = $_POST["sql_query"];

    $db = connect();

    if (!$db) {
        $query_answer["Error"] = "Couldn't connect to the database";
        return;
    }

    if (!check_user($db, $user_id, $token, $query_answer)) {
        return;
    }

    $sql_result = mysqli_query($db, $sql_query);

    if (!$sql_result) {
        $query_answer["Error"] = "Can't do sql query";
        return;
    }

    $query_answer = mysqli_fetch_all($sql_result);
}

$query_answer = ["file" => "makequery.php"];
makequery($query_answer);

echo json_encode($query_answer);