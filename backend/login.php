<?php // login.php

include_once("functions.php");

header('Content-Type: application/json');

function login(&$query_answer) {
	if (!isset($_POST["handle"]) || !isset($_POST["password"])) {
		$query_answer["Error"] = "There are not all post-parameters";
		return;
	}

    $handle = $_POST["handle"];
    $password = $_POST["password"];
	
	$db = connect ();
	if (!$db) {
		$query_answer["Error"] = "Couldn't connect to database";
		return;
	}
	
	$sql = "SELECT id ".
        "FROM users ".
		"WHERE handle = '$handle'";
	$sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Database error while checking handle";
        return;
    }
	
	if (mysqli_fetch_assoc($sql_result) != null) {
	    $query_answer["Error"] = "The user with this handle not exist";
	    return;
    }
    
    $user_id = $sql_result["id"];

	$new_token = create_token();

    $sql = "SELECT * ".
        "FROM connects ".
        "WHERE token = '$new_token'";

    while (mysqli_fetch_assoc(mysqli_query($db, $sql)) != null) {
        $new_token = create_token();
        $sql = "SELECT * ".
            "FROM connects ".
            "WHERE token = '$new_token'";
    }

    $sql = "INSERT ".
        "INTO connects(token, token_time, user_id) ".
        "VALUES('$new_token', ".time().", '$user_id');";
    $sql_result = mysqli_query($db, $sql);

    if (!$sql_result) {
        $query_answer["Error"] = "Can't insert new token into database";
        return;
    }

    $query_answer["token"] = $new_token;
}

$query_answer = ["file" => "login.php"];
login($query_answer);

echo json_encode($query_answer);
    
    