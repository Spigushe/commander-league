<?php
# This site is buit using the MVC architecture
require_once "router.php";

Route(array_merge($_GET,$_POST));
