<?php
/*
 * This script get info about the user by their handle (id, name and email)
 * This script require 1 poat-parameter: handle
 */

header('Content-Type: application/json');

include_once("functions.php");

function get_info(&$query_answer) {
    if (!isset($_POST["handle"])) {
        $query_answer["Error"] = ["id" => 3, "title" => "There are not any require post-arguments"];
        return;
    }

    $handle = $_POST["handle"];

    $db = connect();
    if (!$db) {
        $query_answer["Error"] = "Couldn't connect to the database";
        return;
    }

    $sql = "SELECT id, name, email ".
        "FROM users ".
        "WHERE handle = '$handle'";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error";
        $query_answer["Database error"] = mysqli_error($db);
        return;
    }

    $sql_result = mysqli_fetch_assoc($sql_result);

    if (!isset($sql_result["id"])) {
        $query_answer["Error"] = [
            "id" => 9,
            "title" => "handle '$handle' does not exist",
        ];
        return;
    }

    $query_answer["res"] = $sql_result;
}

$query_answer = [];
get_info($query_answer);

echo json_encode($query_answer);