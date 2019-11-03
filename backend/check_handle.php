<?php // check_handle.php
/*
 * This script check if the handle is exist
 * This script require 1 post-parameter: "handle"
 */

header('Content-Type: application/json');

include_once("functions.php");

function check_handle(&$query_answer) {
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

    $sql = "SELECT * FROM users WHERE handle = '$handle'";
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
        $query_answer["res"] = 1;
        $query_answer["Good"] = "The handle is free";
        return;
    }

    $query_answer["res"] = 0;
    $query_answer["Good"] = "The handle busy";
}

$query_answer = [];
check_handle($query_answer);

echo json_encode($query_answer);
