#!/usr/bin/perl -w

# this cgi is for display other users infos when user search users

# this entrie assignment,I use currentUser to store user who has logged in
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

$cgi = new CGI;

$n = $cgi->param('n');
$currentUser=$cgi->param('currentUser');
sub main() {
    # print start of HTML ASAP to assist debugging if there is an error in the script
    print page_header();
    
   
	# Now tell CGI::Carp to embed any warning in HTML
	warningsToBrowser(1);
	# define some global variables
	$debug = 1;
	$dataset_size = "medium"; 
	$users_dir = "dataset-$dataset_size/users";   
	@users = sort(glob("$users_dir/*"));
    $user_to_show  = $users[$n % @users];
    $user_to_show=~s/dataset-medium\/users\///g;
    $owner = $user_to_show;
    #since I only have page ID, use find id method to find name for owener

    
	print "Welcome to Bitter,$currentUser!!!!!<br>\n";
    listen_to();
    $status=listen_button(); # listen button only tells which kind of button I should Print
    user_page($n,$status);#user page also prints button
	print page_trailer();


}

# listen to make response to defined values
sub listen_to{
	my $file="dataset-$dataset_size/users/$currentUser/details.txt";
	if(defined param('listen')){
		$old = $file;
	    $temp = "dataset-$dataset_size/users/$currentUser/temp.txt";
	    open(OLD, "< $old")         or die "can't open $old: $!";
	    open NEW,'>'.$temp;
	    # Correct typos, preserving case
	    while ($line=<OLD>) {
	        if($line=~/listens: /){
	        	chomp $line;
	        	$line=$line." ".$owner."\n";
	        }
	        print NEW "$line";
	    }
	    close(OLD);                 
	    close(NEW);               
	    unlink $old;
	    rename($temp, $old);

	}elsif(defined param('unlisten')){
		$old = $file;
	    $temp = "dataset-$dataset_size/users/$currentUser/temp.txt";
	    open(OLD, "< $old")         or die "can't open $old: $!";
	    open NEW,'>'.$temp;
	    # Correct typos, preserving case
	    while ($line=<OLD>) {
	        if($line=~/listens: /){
	        	chomp $line;
	        	$line=~s/listens: //;
	        	my @users = split / /,$line;
	        	my @newUsers=();
	        	foreach $user (@users) {
	        		if($user=~m/$owner/g){
	        			#do nothing
	        		}else{
	        			push @newUsers,$user;
	        		}
	        	}
	        	my $print = "listens:";
	        	foreach $user(@newUsers){
	        		$print=$print." ".$user;
	        	}
	        	$print=$print."\n";
	        	print NEW "$print";
	        }else{
	        	print NEW "$line";
	        }
	    }
	    close(OLD);                 
	    close(NEW);               
	    unlink $old;
	    rename($temp, $old);
	}

}

sub listen_button{
	#find page'owner's name
    my $status=0;#0 means not listen now
    my $file="dataset-$dataset_size/users/$currentUser/details.txt";
    open my $p, "$file";
    while($line=<$p>){
    	chomp $line;
    	if($line=~/listens: /){
    		if($line=~m/$owner/g){
    			$status=1;
    		}else{
    			$status=0;
    		}
    	}
    }
    return $status;
}



sub user_page {
    my $n = $_[0];
    my $status = $_[1];
    my @users = sort(glob("$users_dir/*"));
    my $user_to_show  = $users[$n % @users];
    my $details_filename = "$user_to_show/details.txt";
    my $profilePic_filename = "$user_to_show/profile.jpg";
    my $bleats_filename = "$user_to_show/bleats.txt";
    open my $p, "$details_filename" or die "can not open $details_filename: $!";
    $details="";
    while($line=<$p>){
        #chomp $line; don't need chomp,keep line separators
        if($line=~/^email:/){
            next;
        }
        if($line=~/^password:/){
            next;
        }
        $details = $details.$line." ";
    }
    #$details = join '', <$p>;
    close $p;

    #put bleat number into an array
    open my $p, "$bleats_filename" or die "can not open $bleats_filename: $!";
    my @bleatsIndexes=();
    my %bleatsHash=();
    my @bleats=();
    while($line=<$p>){
    	#chomp $line;
    	if($line=~/\d{10}/){
    		push @bleatsIndexes,$line;
    	}
    }
    close $p;

    #put actual bleats into an array
    foreach $bleatIndex(@bleatsIndexes){
    	$bleatAddress="dataset-$dataset_size/bleats/$bleatIndex";#file address
    	open my $p, "$bleatAddress" or die "can not open $bleatAddress: $!";
    	my $time = 0;
    	my $post = '';
    	while($line=<$p>){
    		if($line=~/^bleat: /){
    			#get rid of bleat: from line
    			$line=~s/^bleat: //g;
	  	 		$post = $line;
    		}
    		if($line=~/^time: /){
    			$line=~s/^time: //;
    			$time = $line;
    		}
    	}
   		close $p;
   		$bleatsHash{$post}=$time;
    }

    #sort bleats hash by time
    #sort keys by values
    @bleats = sort {$bleatsHash{$b}<=>$bleatsHash{$a}} keys %bleatsHash;

    my $bleatPrint = join('', @bleats);
    my $next_user = $n + 1;
	if($status==1){
		print <<eof;
<form method="POST" action="">

	<input type="hidden" name="n" value="$n">
	<input type="hidden" name="currentUser" value="$currentUser">
	<input type="submit" name="unlisten" value="Unlisten">
</form>
<div class="bitter_user_details">
<img src= "$profilePic_filename"alt=""/>
$details
Bleats:

$bleatPrint
</div>
<p>
eof
	}else{
		print <<eof;
<form method="POST" action="">
	<input type="hidden" name="n" value="$n">
	<input type="hidden" name="currentUser" value="$currentUser">
	<input type="submit" name="listen" value="Listen">
</form>
<div class="bitter_user_details">
<img src= "$profilePic_filename"alt=""/>
$details
Bleats:

$bleatPrint
</div>
<p>
eof
	}
}
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}
sub page_header {
    return <<eof
Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<title>Bitter</title>
<link href="bitter.css" rel="stylesheet">
</head>
<body>
<div class="bitter_heading">
Bitter
</div>
eof
}
main();