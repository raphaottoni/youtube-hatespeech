require 'csv'
require 'pry'
require 'awesome_print'

biases = Hash::new

CSV.foreach(ARGV[0], :headers=>true) do |row|
  row['youtube_channel'] = "https://www.youtube.com/channel/#{row['youtube_channel']}"
  row['viewCount'] = row['viewCount'].to_i
  row['subscribersCount'] = row['subscribersCount'].to_i
  row['videoCount'] = row['videoCount'].to_i

  if biases.key?(row['bias'])
    biases[row['bias']] << row
  else
    biases[row['bias']] = Array::new
    biases[row['bias']] << row
  end
end

biases.each do |key, value|
  biases[key].sort! do |a, b|
    [b['subscribersCount'], b['viewCount'], b['videoCount']] <=> [a['subscribersCount'], a['viewCount'], a['videoCount']]
  end

  CSV.open("../data/biggest-channels-#{key}.csv", 'w') do |out|
    out << ['media', 'bias', 'youtubeChannel', 'viewCount', 'subscribersCount', 'videoCount']

    biases[key].each do |channel|
      if(channel['subscribersCount'] < 100000) then break end
      out << channel
    end
  end
end

