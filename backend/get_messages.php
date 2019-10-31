<?php
/*
 *  This script send SQL query to database from the machine describing by token and user id
 *  This script require 3 post-arguments: "user_id", "token" and "sql_query"
 */

header('Content-Type: application/json');

include_once("functions.php");

function get_messages(&$query_answer) {
    if (!isset($_POST["handle"]) || !isset($_POST["token"]) || !isset($_POST["to_handle"])) {
        $query_answer["Error"] = ["id" => 3, "title" => "There are not any require post-arguments"];
        return;
    }

    $to_handle = $_POST["to_handle"];
    $handle = $_POST["handle"];
    $token = $_POST["token"];

    $db = connect();
    if (!$db) {
        $query_answer["Error"] = "Couldn't connect to the database";
        return;
    }

    /*$user_id = get_id_from_handle($db, $handle, $query_answer);
    if (!$user_id) {
        return;
    }

    $to_id = get_id_from_handle($db, $to_handle, $query_answer);
    if (!$to_id) {
        return;
    }

    if (!check_user($db, $user_id, $token, $query_answer)) {
        return;
    }*/

    $sql = "SELECT from_handle, to_handle, text, time ".
        "FROM messages ".
        "WHERE (from_handle = '$handle' AND to_handle = '$to_handle') ".
        "OR (from_handle = '$to_handle' AND to_handle = '$handle')";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error";
        $query_answer["Database error"] = mysqli_error($db);
        return;
    }

    $query_answer["Good"] = "All good";
    $query_answer["result"] = mysqli_fetch_all($sql_result);
}

$query_answer = [];
get_messages($query_answer);

echo json_encode($query_answer);
