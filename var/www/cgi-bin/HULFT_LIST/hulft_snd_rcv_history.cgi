#!/usr/bin/perl

#-----#-----#-----MUST-----#-----#-----#
use strict;
use warnings;
#-----#-----#-----MUST-----#-----#-----#

# 00-モジュールの読み込み
#
#-----#-----#------------------------------------------------------#-----#-----#
use CGI;
use CGI::Carp('fatalsToBrowser');
use Data::Dumper;

my $q = CGI->new;
$q ->charset('Shift_JIS');

# 01-変数の定義(パラメータとしてもらってきたもの）
#
#-----#-----#------------------------------------------------------#-----#-----#
my $from_date         = $q ->param('from_date');
my $to_date           = $q ->param('to_date');
my $snd_rcv_flag      = $q ->param('snd_rcv_flag');
my $hulft_server_name = $q ->param('hulft_server_name');
my $redirect_file     = '/var/www/cgi-bin/HULFT_LIST/cattest.txt';
my $hulft_infos       = [];

# パラメータの渡し方テスト中
#
#-----#-----#------------------------------------------------------#-----#-----#
print $q->header;
print "$from_date"."<br>";
print "$to_date"."<br>";
print "$snd_rcv_flag"."<br>";
print "$hulft_server_name","<br>";

# 選択項目によるロジック test中
#
#-----#-----#------------------------------------------------------#-----#-----#
# [----------]を選択した場合のロジック
if ( $hulft_server_name eq "----------" ){
  if( $snd_rcv_flag eq "snd"){
   &MAKE_ARRAY_FROM_HULFT_RECORDS;
   print '<font size="2">';
   print "FILEID    HOST NAME  START DAY   START TIME  END TIME  RECORDS STATUS  CONNECT"."<br>";
   print "</font>";
   print '<font size="2" color="#FF0000">';
   &PRINT_HULFT_INFOS('ABEND');
   print "</font>";
   print '<font size="2">';
   print "FILEID    HOST NAME  START DAY   START TIME  END TIME  RECORDS STATUS  CONNECT"."<br>";
   print "</font>";
   print '<font size="2" color="#0000FF">';
   &PRINT_HULFT_INFOS('NORMALEND');
   print "</font>";
  }elsif( $snd_rcv_flag eq "rcv"){
   print 'RCVSEIKOU';
  }
}

# [---------]を選択した場合のロジック
if ( $hulft_server_name eq "------------" ){
  if( $snd_rcv_flag eq "snd"){
   print 'SNDSEIKOU';
  }elsif( $snd_rcv_flag eq "rcv"){
   print 'RCVSEIKOU';
  }
}

# コマンド実行->テキストにリダイレクト->整形処理
#
sub MAKE_ARRAY_FROM_HULFT_RECORDS{
# system("echo $to_date >> $redirect_file" );
# `echo $to_date >> $redirect_file `;
#if ( $snd_rcv_flag eq "snd" ){
# my $snd_rcv_flag = "-s";
# print "snd no header";
#}else{
# my $snd_rcv_flag = "-r";
# print "rcv no header";
#};
#`ssh -l hulft $hulft_server_name utllist "$snd_rcv_flag" -from "$from_date" -to "to_date" >> $redirect_file`;
#my $redirect_result=`ssh -l hulft $hulft_server_name utllist "$snd_rcv_flag" -from "$from_date" -to "to_date" >> $redirect_file`;
 open (my $REDIRECT_FILE,'<',$redirect_file);
 while (my $hulft_record = <$REDIRECT_FILE>) {
  next if $. == 1 ;
  next if $. == 2 ;
  chomp($hulft_record);
  my @hulft_fileds = split(/\s+/, $hulft_record);
  my $hash_hulft_record = {};
  $hash_hulft_record->{FILEID}     = $hulft_fileds[0];
  $hash_hulft_record->{HOSTNAME}   = $hulft_fileds[1];
  $hash_hulft_record->{STARTDAY}   = $hulft_fileds[2];
  $hash_hulft_record->{STARTTIME}  = $hulft_fileds[3];
  $hash_hulft_record->{ENDTIME}    = $hulft_fileds[4];
  $hash_hulft_record->{RECORDS}    = $hulft_fileds[5];
  $hash_hulft_record->{STATUS}     = $hulft_fileds[6];
  $hash_hulft_record->{CONNECT}    = $hulft_fileds[7];
  print "\n";
  push @$hulft_infos, $hash_hulft_record;
 };
};

# 出力処理
#
sub PRINT_HULFT_INFOS{
 $ARGV = shift @_; #引数の代入処理
 foreach my $hulft_fileds (@$hulft_infos){
         my @hulft_record = (
                             $hulft_fileds->{FILEID},
                             $hulft_fileds->{HOSTNAME},
                             $hulft_fileds->{STARTDAY},
                             $hulft_fileds->{STARTTIME},
                             $hulft_fileds->{ENDTIME},
                             $hulft_fileds->{RECORDS},
                             $hulft_fileds->{STATUS},
                             $hulft_fileds->{CONNECT}
        );
        if ( $ARGV eq 'NORMALEND' ) {
         next if ( $hulft_fileds->{STATUS} ne '0000-0000' );
         print join('    ',@hulft_record)."\n";
        } elsif ( $ARGV eq 'ABEND' ) {
         next if ( $hulft_fileds->{STATUS} eq '0000-0000' );
         print join('    ',@hulft_record)."\n";
        }
  print "<br>";
 };
};
