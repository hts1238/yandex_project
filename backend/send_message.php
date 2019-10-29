<?php
/*
 *  This script send SQL query to database from the machine describing by token and user id
 *  This script require 3 post-arguments: "user_id", "token" and "sql_query"
 */

header('Content-Type: application/json');

include_once("functions.php");

function send_message(&$query_answer) {
    if (!isset($_POST["from_handle"]) || !isset($_POST["token"]) || !isset($_POST["to_handle"]) || !isset($_POST["text"])) {
        $query_answer["Error"] = ["id" => 3, "title" => "There are not any require post-arguments"];
        return;
    }

    $from_handle = $_POST["from_handle"];
    $token = $_POST["token"];
    $to_handle = $_POST["to_handle"];
    $text = $_POST["text"];

    $db = connect();

    if (!$db) {
        $query_answer["Error"] = "Couldn't connect to the database";
        return;
    }

    $user_id = get_id_from_handle($db, $from_handle, $query_answer);
    if (!$user_id) {
        return;
    }

    $to_id = get_id_from_handle($db, $to_handle, $query_answer);
    if (!$to_id) {
        return;
    }

    if (!check_user($db, $user_id, $token, $query_answer)) {
        return;
    }

    $sql = "INSERT ".
        "INTO messages(from_id, to_id, text, time) ".
        "VALUES($user_id, $to_id, '$text', ".time().")";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error";
        $query_answer["Database error"] = mysqli_error($db);
        return;
    }

    $query_answer["Good"] = "All good";
}

$query_answer = [];
send_message($query_answer);

echo json_encode($query_answer);