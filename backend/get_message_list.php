<?php // get_message_list.php
/*
 * This script give a message list included all users which the user has correspondence with
 * This script require 2 post-parameters: "handle" and "token"
 */

header('Content-Type: application/json');

include_once("functions.php");

function get_message_list(&$query_answer) {
    if (!isset($_POST["handle"]) || !isset($_POST["token"])) {
        $query_answer["Error"] = ["id" => 3, "title" => "There are not any require post-arguments"];
        return;
    }

    $handle = $_POST["handle"];
    $token = $_POST["token"];

    $db = connect();
    if (!$db) {
        $query_answer["Error"] = "Couldn't connect to the database";
        return;
    }

    $id = get_id_from_handle($db, $handle, $query_answer);
    if (!id) {
        return;
    }

    if (!check_user($db, $id, $token, $query_answer)) {
        return;
    }

    $sql = "SELECT from_handle, to_handle, text, time ".
        "FROM messages ".
        "WHERE (from_handle = '$handle' OR to_handle = '$handle')";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error";
        $query_answer["Database error"] = mysqli_error($db);
        return;
    }

    $sql_result = mysqli_fetch_all($sql_result);

    foreach ($sql_result as $message) {
        if ($message[1] == $handle) {
            $query_answer[$message[0]] = [
                "type" => "incomming",
                "text" => $message[2],
                "time" => $message[3],
            ];
        }
        if ($message[0] == $handle) {
            $query_answer[$message[1]] = [
                "type" => "outcomming",
                "text" => $message[2],
                "time" => $message[3],
            ];
        }
    }
}

$query_answer = [];
get_message_list($query_answer);

echo json_encode($query_answer);
