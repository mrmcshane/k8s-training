<?php
// definately not a clone of icanhazip.com
// check if the url is curled or visited normally
if(preg_match("/curl|libcurl/", $_SERVER['HTTP_USER_AGENT'])){
   
   // if called, no styling
   echo $_SERVER["REMOTE_ADDR"];
   echo "\r\n";
}
else{
   // if not curled, make it pretty
   echo '<pre>';
   echo $_SERVER["REMOTE_ADDR"];
   echo '</pre>';
   echo "\r\n";
}
?>