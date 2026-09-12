#!/usr/bin/env ruby

line = ARGV[0]
m = line.match(/\[from:(.*?)\].*\[to:(.*?)\].*\[flags:(.*?)\]/)
if m
  sender, receiver, flags = m.captures
  puts "#{sender}, #{receiver}, #{flags}"
end
