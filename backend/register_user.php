<?php // register_user.php
/*
 * This script register the user in database, but does not login
 * This script require 4 post-parameters: "name", "handle", "email" and "password"
 */

include_once("functions.php");

header('Content-Type: application/json');

function register_user(&$query_answer) {
	if (!isset($_POST["name"]) || !isset($_POST["handle"]) || !isset($_POST["email"]) || !isset($_POST["password"])) {
		$query_answer["Error"] = "There are not all post-parameters";
		return;
	}

	$name = $_POST["name"];
    $handle = $_POST["handle"];
    $email = $_POST["email"];
    $password = $_POST["password"];
	
	$db = connect ();
	if (!$db) {
		$query_answer["Error"] = "Couldn't connect to database";
		return;
	}

    if (!validate_data($name, $handle, $email, $password)) {
        $query_answer["Error"] = "invalid handle or password";
    }
	
	$sql = "SELECT * ".
        "FROM users ".
		"WHERE handle = '$handle'";
	$sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error while checking handle";
        return;
    }
	
	if (mysqli_fetch_assoc($sql_result) != null) {
	    $query_answer["Error"] = "The user with this handle has already been created";
	    return;
    }

	$sql = "INSERT ".
        "INTO users(name, handle, email, password) ".
        "VALUES('$name', '$handle', '$email', '$password')";
	$sql_result = mysqli_query($db, $sql);

	if (!$sql_result) {
	    $query_answer["Error"] = "Database while adding new user";
	    return;
    }

    $query_answer["Good"] = "All good";
}

$query_answer = ["file" => "register.php"];
register_user($query_answer);

echo json_encode($query_answer);
