<?php
function Route ($path) {
	if (isset($path['action'])) {
		echo "Starting ".$path['action'];
	} else {
		echo "Hello World!";
	}
}
