Nagios Plugins :: nagios-plugins
================================

Description
------------

`nagios-plugins` pretend to be a collection of various customized plugins that my
mates and I, have written and expanded over the last 2 years or so, working a monitoring
area in a pretty popular company.

They have mostly been written in Perl/Bash.

Overview of Available Plugins
-----------------------------

###log4j\_parser.pl  
This plugin retrieves data from log lines matching labels and columns in a time frame,
also you can set thresholds for each of label.

####Usage and Help:  

<pre>
  Usage: log4j_parser.pl -p|--path complete_path_to_log_file -s|--string labels_to_parse [-m|--minutes <ammount of minutes before the actual date to set the time frame>] [-C|--column <name of the column to retrieve the data>] [-d|--date-format <date format>] [-n|--column-names <set names for each log column>] [-w|--warning <warning threshold>] [-c|--critical <critical threshold>] [-?|--usage] [-V|--version] [-h|--help] [-t|--timeout=<timeout>]

 -?, --usage
   Print usage information
 -h, --help
   Print detailed help screen
 -V, --version
   Print version information
 --extra-opts=[section][@file]
   Read options from an ini file. See http://nagiosplugins.org/extra-opts for usage
 -p, --path=STRING
   Complete path to the log file
 -s, --string=STRING
   Labels or tags to search in the log file, separated with "+" from each other
 -m, --minutes=INTEGER
   Ammount of minutes before the actual date to set a range of time. Default 1 min
 -C, --column=STRING
   Name of the column to pick up the value. Default value: Count
 -d, --date-format=STRING
   Date format of the log file based on POSIX strftime. Default is "%Y-%m-%d %H:%M:"
 -n, --column-names=STRING
   You can set names for each log column, separated with "+" from each other. Default value is: 0+1+2+3+4+5
 -c, --critical=STRING
   Values for the Critical Thresholds separated with "+". The ammount of given criticals thresholds must match the ammount of labels to check. http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
 -w, --warning=STRING
   Values for the Warning Thresholds separated with "+". The ammount of given warnings thresholds must match the ammount of labels to check. http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
 -t, --timeout=INTEGER
   Seconds before plugin times out (default: 15)
 -v, --verbose
   Show details for command-line debugging (can repeat up to 3 times)
</pre>

####Example of use:  
  Suppose you have a log file named `log_file.log` with the following format:
  
    Performance Statistics   2013-08-26 17:04:00 - 2013-08-26 17:05:00
    Tag                           Avg(ms)         Min         Max     Std Dev       Count
    label1                            0.0           0           0         0.0           2
    label2                            0.5           0           1         0.5           2
    label3                            0.2           0         134         2.9        2588
    label4                            5.0           5           5         0.0           1
    label5                           12.3          10          18         2.2          15
    label6                           38.1           0         996        63.3        1765
    label7                            0.4           0          24         2.1         192
  
  So, if you would like to parse Avg time \(first column\) of, for example, label1 and label5:
  
  
    $ ./log4j_parser.pl -p 'log_file.log' -s 'label1+label5' -C 1
    LOG4J_PARSER OK - All stats retrieved | label1=0.0;; label5=12.3;;
  

License and Author
------------------

Author:: Exequiel Pierotto <exequiel.pierotto@gmail.com>  
Author:: Enrique Garbi <quique@enriquegarbi.com.ar>


Unless stated otherwise at the top of the script of its help output, all scripts
are:

    Copyright (c) 2004 - 2012, Barry O'Donovan <info@opensolutions.ie>
    Copyright (c) 2004 - 2012, Open Source Solutions Limited <info@opensolutions.ie>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

     * Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

     * Redistributions in binary form must reproduce the above copyright notice, this
       list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution.

     * Neither the name of Open Solutions nor the names of its contributors may be
       used to endorse or promote products derived from this software without
       specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
    OF THE POSSIBILITY OF SUCH DAMAGE.


