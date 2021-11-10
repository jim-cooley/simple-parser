1..2    # UNDONE: parses incorrectly, generating Float(1.0), Range lexeme is truncated but still parses to Range()
a..b
[1..2]  # UNDONE: same issue, 1..2 becomes 1.0 .. 2
[a..b, 1..2]
today-2y..today
(today-2y)..today
{ 'train': today-2y..today }
{ 'train': (today-2y)..today }
[3,5,10..20,28] # UNDONE: 10..20 parses to None