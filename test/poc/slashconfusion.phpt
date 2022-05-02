<?php

$url = "https:///evil.com";
$parsed = parse_url($url);

# print_r($parsed);

# Check if the URL is blacklisted
if ($parsed["host"] == "evil.com") {
	print("URL not allowed.\n");
	exit();
}

$curl = curl_init($url);
$data = curl_exec($curl);

# print($data);

?>
