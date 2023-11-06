#!/usr/bin/env perl
use strict;
use warnings;

use Path::Tiny;
use LWP::UserAgent;
use JSON;

# Usage

# Check if folder names are provided as command-line arguments
if (@ARGV == 0) {
    die "Usage: $0 folder_name1 folder_name2 ...\n";
}

# Loop over folder name arguments
foreach my $folder_name (@ARGV) {
    my $current_dir = path($folder_name)->mkdir;

    my ($parent_dir, $is_git) = get_git_repo_name($current_dir);
    my $readme_file = $current_dir->child('README.md');

    if (!$readme_file->is_file) {
        create_readme_file($readme_file, $parent_dir, $current_dir, $is_git);
    } else {
        print "README.md already exists in '$current_dir'. Skipping.\n";
    }
}

sub create_readme_file {
    my ($readme_file, $parent_dir, $current_dir, $is_git) = @_;
    my $author_name = $is_git ? get_author_name($current_dir) : "FourtyThree";
    # my $author_name = "Unknown-Author";
    my $quote = fetch_fortune_quote();

    my $content = <<"END";
# $parent_dir

## $current_dir

### Description

* **TODO**

### Resources

* **TODO**

### Learning Objectives

* **TODO**

### Environment

* Languages: * **TODO**
* OS: Ubuntu 22.04 LTS
* Style guidelines: * **TODO**


## Author

* [$author_name](https://www.github.com/$author_name/$parent_dir/$current_dir)

## [Fortune Cookie](http://yerkee.com/)

```
$quote
```
END

    $readme_file->spew_utf8($content);

    if ($is_git) {
        print "README.md created in '$current_dir' (Repo: $parent_dir).\n";
    } else {
        print "README.md created in '$current_dir' (Not a Git Repository).\n";
    }
}


# Check if the Path is under a git repo.
sub get_git_repo_name {
    my ($current_dir) = @_;
    my $path = path($current_dir)->parent->realpath;

    if (-d $path) {
        if (-d $path->child('.git')) {
            # It's a Git repository
            my $parent_dir = $path->basename;
            my $is_git = 1;
            return ($parent_dir, $is_git);
        } else {
            # It's not a Git repository
            my $is_git = 0;
            my $parent_dir = path($current_dir)->realpath->basename;
            return ($parent_dir, $is_git);
        }
    } else {
        die "Invalid directory: $current_dir";
    }
}

sub get_author_name {
    my ($current_dir) = @_;
    my $log_output = `git -C "$current_dir" log --format='%aN'`;
    my @author_names = split /\n/, $log_output;
    my $author_name = $author_names[0] || "Unknown-Author";
    chomp($author_name);
    return $author_name;
}

sub fetch_fortune_quote {
    my $ua = LWP::UserAgent->new;
    my $response = $ua->get('http://yerkee.com/api/fortune');

    if ($response->is_success) {
        my $quote = decode_json($response->decoded_content)->{fortune};
        print "Quote fetched successfully.\n";
        return $quote;
    } else {
        print "Fetching quote failed: " . $response->status_line . "\n";
        return '';
    }
}
