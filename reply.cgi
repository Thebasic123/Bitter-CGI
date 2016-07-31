#!/usr/bin/perl -w

# this cgi will help user get into a reply page, which includes message and
#message id 
use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;

$cgi = new CGI;

#use hidden value to store user info and bleat message
$currentUser = $cgi->param('currentUser');
$bleat = $cgi->param('bleat');

sub main{
	print page_header();
	# Now tell CGI::Carp to embed any warning in HTML
	warningsToBrowser(1);
	# define some global variables
	$debug = 1;
	$dataset_size = "medium"; 
	$users_dir = "dataset-$dataset_size/users";
    $bleat_id = find_id();
    print "Hi,$currentUser\n";
	send_bleat();
	print page_trailer();
}

#find bleat id for replied message
sub find_id{
    my $bleat_dir="dataset-$dataset_size/bleats";
    my @bleats = sort(glob("$bleat_dir/*"));
    my $address;
    my $id;
    foreach $file(@bleats){
        open my $p, "$file";
        while($line=<$p>){
            chomp $line;
            if($line=~/^bleat: /){
                $line=~s/^bleat: //;
                if($line=~m/$bleat/g){
                    $address = $file;
                }
            }
        }
    }
    ($id)=$address=~m/\d{10}/g;
    return $id;

}
#send message 
sub send_bleat{
    my $post = param('reply_bleat');
    my $currentUser = $currentUser;
    $post = substr $post,0,142;#limit bleat within 142 words
    my $bleat_dir="dataset-$dataset_size/bleats";
    my @bleats = sort(glob("$bleat_dir/*"));
    my @numbers=();
    #find the larggest number in file
    if($post ne ""){
        foreach $file(@bleats){
            ($number)=$file=~m/\d{10}/g;
            push @numbers,$number;
        }
        my $larggest=$numbers[0];
        foreach $element(@numbers){
            if($element>=$larggest){
                $larggest=$element;
            }
        }
        my $newBleat=$larggest+1;

        #get time 
        $epoc = time();
        my $time = $epoc;

        #create a new bleat
        my $newFileAddress = "$bleat_dir/$newBleat";
        open FILE,'>'.$newFileAddress;
        print FILE "username: $currentUser\n";
        print FILE "in_reply_to: $bleat_id\n";
        print FILE "time: $time\n";
        print FILE "bleat: $post\n";
        close FILE;
        #add new bleat number to user folder
        my $user_bleat_address = "dataset-$dataset_size/users/$currentUser/bleats.txt";
        open FILE,'>>'.$user_bleat_address;
        print FILE "$newBleat\n";
        close FILE;
	}


    print <<eof
<form method="post">
Reply to Bleat ($bleat_id $bleat): <input type="text" name="reply_bleat">

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="hidden" name="currentUser" value="$currentUser">
<input type="hidden" name="bleat" value="$bleat">
<input type="submit" class="btn btn-link" value="Reply">

</form>

eof
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


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}
main();

