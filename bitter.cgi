#!/usr/bin/perl -w 

#author : FUFU HU
# this entrie assignment,I use currentUser to store user who has logged in



use CGI qw/:all/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session;



sub main() {
    # print start of HTML ASAP to assist debugging if there is an error in the script
    print page_header();
    
   
	# Now tell CGI::Carp to embed any warning in HTML
	warningsToBrowser(1);
	$username = param('username') || '';
	$password = param('password') || '';
 	# define some global variables
	$debug = 1;
	$dataset_size = "medium"; 
	$users_dir = "dataset-$dataset_size/users";   
    logFunction();





}

# log function actully calls other functions to arrange interface 
#if user has logged in just print user info
# if user provides wrong password, let them input again
#I use hidden value to check things
sub logFunction{
     $username = param('username') || '';
     $password = param('password') || '';
    $currentUser = param('currentUser');
    if($username){
        my $detail_address= "$users_dir/$username/details.txt";
        open my $p, "$detail_address";
        my $correct_password="";
        while ($line=<$p>) {
            if($line=~ /password: /){
                $line=~s/password: //;
                $correct_password = $line;
            }
        }
        close $p;
        chomp $correct_password;
        if($password eq $correct_password){
            print "Welcome to Bitter,$username!!!!";

            #change hidden current user
            $currentUser = $username;
            send_bleat($username);
            search_user($username);
            search_bleat($username);
            home_page($username);
            display_relevant($username);
            print user_page($username);
            print page_trailer();

        }else{ #if users provides wrong password or username doesn't exist
            print $password;
            print $correct_password;
            print <<eof
Wrong Password or Username does not exist !!!!!
<form method="post" action="">
Username: <input type="text" name="username">

Password: <input type="password" name="password">
<input type="hidden" name="currentUser" value="$currentUser">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="submit"class="btn btn-link" value="Login">
</form>

eof

        }
    }else{ 
        if($currentUser ne ''){ # if there is a current user
            print <<eof;
<form method="post" action="">
<input type="hidden" name="currentUser" value="$username">
</form>

eof
            print "Welcome to Bitter,$currentUser!!!!";
            send_bleat($currentUser);
            search_user($currentUser);
            search_bleat($currentUser);
            home_page($currentUser);
            display_relevant($currentUser);
            print user_page($currentUser);
            print page_trailer();

        }else{ # if there isn't a current user and user hasn't provided info
            print <<eof
<form method="post" action="">
Username: <input type="text" name="username">

Password: <input type="password" name="password">
<input type="hidden" name="currentUser" value="$currentUser">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="submit"class="btn btn-link" value="Login">
</form>

eof

        }

    }
}

#search user prints href links to user_page.cgi with current user and the other user id as 
#parameter
sub search_user{
    my $username=$_[0];
    my $searchName = param('searchName');
    my $n = 0;
    my @users = sort(glob("$users_dir/*"));
    my @names=();
    my @numbers=();
    if(defined $searchName){
        foreach $userDetail(@users){
            $userDetail=$userDetail."/details.txt";
            open my $p, "$userDetail";
            while($line=<$p>){
                chomp $line;
                if($line=~/username: /){
                    $line =~s/username: / /;
                    if($line=~m/$searchName/g){
                        push @names,$line;
                        push @numbers,$n;
                    }
                }elsif($line=~/full_name: /){
                    $line =~ s/full_name: / /;
                    if($line=~m/$searchName/g){
                        push @names,$line;
                        push @numbers,$n;
                    }
                }
            }
            $n = $n+1;
        }


    }
    $linkToUsers="";
    for (my $i=0;$i<@names;$i++){
        $linkToUsers=$linkToUsers.'<a href="user_page.cgi?'."n=$numbers[$i]&currentUser=$username".'">'."$names[$i] </a>";
    }


    print <<eof
<form method="post">
Search Username: <input type="text" name="searchName">
<input type="hidden" name="currentUser" value="$username">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="submit" class="btn btn-link" value="Search User">

$linkToUsers
</form>

eof
}

#similarly with search user, print extra href link fo reply, 
#jump to reply.cgi
sub search_bleat {
    my $username=$_[0];
    my $search_string = param('searchString')||"";
    my $bleat_dir="dataset-$dataset_size/bleats";
    my @bleats = sort(glob("$bleat_dir/*"));
    my @result =();
    foreach $bleatFile(@bleats){
        open my $p, "$bleatFile";
        while($line=<$p>){
            chomp $line;
            if($line=~/^bleat: /){
                $line=~s/^bleat: //;
                if($line=~m/$search_string/g){
                    push @result,$line;
                }
            }
        }
    }
    #print results in different lines
    $printBleats="";
    foreach $post(@result){
        $printBleats=$printBleats."<br>$post\n".'<a href="reply.cgi?'."currentUser=$username&bleat=$post".'">'."Reply </a>";
    }

    print <<eof
<form method="post">
Search Bleats: <input type="text" name="searchString">
<input type="hidden" name="currentUser" value="$username">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="submit" class="btn btn-link" value="Search Bleats">

$printBleats

</form>

eof


}
#home page function prints some self info

sub home_page{
    my $currentUser=$_[0];
    my $picAddress="$users_dir/$currentUser/profile.jpg";
    my $detail_address="$users_dir/$currentUser/details.txt";
    open my $p, "$detail_address" or die "can not open $details_filename: $!";
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
    close $p;
    print <<eof;
<div class="bitter_user_details">
<img src= "$picAddress"alt=""/>
$details
</div>
eof
}



#dispaly relevant bleats, pass in current user
sub display_relevant{
    my $currentUser = $_[0];

    #my $currentUser = param('currentUser');
    my $detail_address = "$users_dir/$currentUser/details.txt";
    my @listenTO=();
    my @display_numbers=();
    open my $p, "$details_address";
    while($line=<$p>){
        chomp $line;
        if($line=~/listens: /){
            $line=~s/listens: //;
            @listenTO = split / /,$line;
        }
    }
    close $p;
    #add user himself to user check list
    push @listenTO,$currentUser;
    foreach $user(@listenTO){
        my $bleats_filename = "$users_dir/$user/bleats.txt";
        open my $p, "$bleats_filename";
        while($line=<$p>){
            chomp $line;
            push @display_numbers,$line;
        }
        close $p;
    }
    #add @ bleats to display list
    my $bleat_dir="dataset-$dataset_size/bleats";
    my @bleats = sort(glob("$bleat_dir/*"));
    foreach $bleat(@bleats){
        open my $p, "$bleat";
        while($line=<$p>){
            chomp $line;
            if($line=~/bleat: /){
                $line=~s/bleat: //;
                #check whether message tagged current user or not
                if($line=~m/$currentUser/g){
                    ($number)=$bleat=~m/\d{10}/g;
                    push @display_numbers,$number;
                }
            }
        }
        close $p;
    }
    my %output;
    foreach $element(@display_numbers){
        my $address = "dataset-$dataset_size/bleats/$element";
        my $key;
        my $value;
        open my $p,"$address";
        while($line=<$p>){
            chomp $line;
            if($line=~/time: /){
                $line=~s/time: //;
                $value=$line;
            }
            if($line=~/bleat: /){
                $line=~s/bleat: //;
                $key=$line;
            }
        }
        $output{$key}=$value;
    }
    my @prints = sort {$output{$b}<=>$bleatsHash{$a}} keys %output;
    #print results in different lines
    my $result="";
    foreach $post(@prints){
        $result=$result."<br>$post\n".'<a href="reply.cgi?'."currentUser=$currentUser&bleat=$post".'">'."Reply </a>";
    }
    print <<eof
<form method="post">
Relevant Bleats:

$result

</form>

eof



}

#send bleat pass in current user
sub send_bleat{

    my $post = param('send_bleat');
    my $currentUser = $_[0];
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
Send Bleat: <input type="text" name="send_bleat">
<input type="hidden" name="currentUser" value="$currentUser">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
<input type="submit" class="btn btn-link" value="Send">

</form>

eof
}

#
# Show unformatted details for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
    my $username=$_[0];
    my $n = param('n') || 0;
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
    return <<eof
<div class="bitter_user_details">
<img src= "$profilePic_filename"alt=""/>
$details
Bleats:

$bleatPrint
</div>
<p>
<form method="POST" action="">
    <input type="hidden" name="currentUser" value="$username">
    <input type="hidden" name="n" value="$next_user">
    <input type="submit" value="Next User" class="bitter_button">
</form>

<form method="POST" action="">
    <input type="submit" value="Log Out" class="bitter_button">
</form>

eof
}


#
# HTML placed at the top of every page
#
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
