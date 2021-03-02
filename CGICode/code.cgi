#! C:\xampp\perl\bin\perl.exe
print "Content-type: text/html\n\n";

use strict;
use warnings;
use DBI;
use JSON; #if not already installed, just run "cpan JSON"
use CGI;
use Data::Dumper;
use XML::Simple;

use CGI ':standard','-debug';
use CGI::Carp qw(fatalsToBrowser);
my $cgi = CGI->new;
print $cgi->header('application/json;charset=UTF-8');

#print $cgi->header('application/json;charset=UTF-8');

my $id = $cgi->param('r');    
#convert  data to JSON
my $id1=decode_json($id);
# print $id;
my $id= $id1->{buffet}[0]->{design_id}[0];
# my $size=$#ar;
my $filename=$id."_output.XML";
# my $filename=$id+$filename;
open(FH, '>', $filename) or die $!;

#print $filename;
# print "<html><body>Hello</body></html>";
my $xml = XMLout($id1);
#print $xml;

my $connection = DBI->connect("DBI:mysql:imageentry3:localhost", "root", "12345");

my $query=$connection->prepare(qq{SELECT COUNT(imagedata) FROM imageentry4 WHERE imageID='$id'});
my $res=$query->execute();
my $ver=$query->fetchrow_array();
# print $ver;
print FH $xml;

if ($ver == 1){
	print qq{Oops! Design No Already Present! Provide a different design no};	
}
else{
	$query = $connection->prepare(qq{INSERT INTO imageentry4 values('$id', '$xml')});
	$query->execute(); 
	print qq{XML Data inserted successfully!};
}

$query->finish();
close(FH);





