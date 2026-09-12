#!/usr/bin/env ruby

ARGF.each_line do |line|
  m = line.match(/\[from:(.*?)\].*\[to:(.*?)\].*\[flags:(.*?)\]/)
  next unless m
  sender, receiver, flags = m.captures
  puts "#{sender}, #{receiver}, #{flags}"
end
