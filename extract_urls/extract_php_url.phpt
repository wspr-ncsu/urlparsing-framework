<?php

$json_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/php.json';
$url_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/libs/php-src/ext/standard/tests/url/urls.inc';
include_once($url_file);

foreach ($urls as $url) {
    $parsed = parse_url($url);
    
    $keys = array('scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment');
    if (isset($parsed["pass"])) {
    	$parsed["password"] = $parsed["pass"];
    	unset($parsed["pass"]);
    }
    foreach ($keys as $key) {
    	if (!isset($parsed[$key])) {
    		$parsed[$key] = "";
    	}
    }
    
    $new_data = array(
		'input' => $url,
		'expected_output' => $parsed
	);
	write_to_file($new_data, $json_file);
}

function write_to_file($new_data, $file) {
	if (!file_exists($file)) {
		$fp = fopen($file, 'w+');
		fwrite($fp, json_encode(array('urls' => []), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
		fclose($fp);
	}
	$data = json_decode(file_get_contents($file), true);
	array_push($data["urls"], $new_data);
	file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
}

?>