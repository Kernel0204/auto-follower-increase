<?php
$mode = $_GET["mode"];

if($mode == "nekonomanako"){
    shell_exec ("/virtual/nekonomanako/python/bin/python3.4 /virtual/nekonomanako/public_html/nekonomanako.shop/spilitualTwitter.py nekonomanako");
}elseif($mode == "dokugaku"){
    shell_exec ("/virtual/nekonomanako/python/bin/python3.4 /virtual/nekonomanako/public_html/nekonomanako.shop/spilitualTwitter.py dokugaku");
}elseif($mode == "shimechansan"){
    shell_exec ("/virtual/nekonomanako/python/bin/python3.4 /virtual/nekonomanako/public_html/nekonomanako.shop/spilitualTwitter.py shimechansan");
}


?>
