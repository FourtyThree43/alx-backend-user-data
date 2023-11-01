#!/usr/bin/env perl

use strict;
use warnings;

my $string_to_input = shift @ARGV;
my $file_extension = shift @ARGV;

# Check if both arguments are provided
if (!$string_to_input || !$file_extension) {
    die "USAGE: $0 <\"INPUT_STR\"> <FILE_TYPE>\n\tex: $0 \"HELLO WORLD\" txt\n";
}

# Get a list of all files with the specified extension in the current directory
my @files = glob("*.$file_extension");
my $file_count = scalar @files;  # Count of files found

if ($file_count > 0) {
    print "Found $file_count file(s) with .$file_extension extension.\n";
    print "Updating: @files\n";
    my @skipped_files;
    my $skipped_count = 0;

    # Iterate over each file
    foreach my $file (@files) {
        # Read the contents of the file
        open(my $fh, '<', $file) or die "Could not open file '$file' $!";
        my @lines = <$fh>;
        close($fh);

       # Skip the file if it already contains the string
       # next if grep { $_ eq "$string_to_input\n" } @lines;
        if (grep { $_ eq "$string_to_input\n" } @lines) {
            push @skipped_files, $file;
            $skipped_count++;
            next;
        }

        # Open the file in write mode
        open($fh, '>>', $file) or die "Could not open file '$file' $!";

        # Add the string to the file
        print $fh "$string_to_input\n";

        # Close the file
        close($fh);
    }
    # Print skipped files and count
    if ($skipped_count > 0) {
      print "Skipped $skipped_count file(s):\n";
      print "$_ " for @skipped_files;
    }

    print "\nDone! Updating .$file_extension files.\n";
} else {
    print "No files found.\n";
}
