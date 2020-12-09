### Define all file directories, it is best not to change

cover = 'files/cover/'
stego = 'files/stego/'

message_extract = 'files/message_extract/'
message_embed = 'files/message_embed/'
message_default = 'files/message.txt'
###

### Need to ensure that the following parameters are defined correctly

# -1: random  0: default  1: exist data
message_choose = -1

# 0: L mode, 1: R channel, 2: G channel, 3: B channel, 4: embedded RGB three channels separately
# Each image can only embed in one channel
# If image is L mode, then image expect to embed in L mode (code=0), otherwise report an error
channel_code = 4
channel = ['L', 'R', 'G', 'B']

# The password used to encrypt the message
password = 's3cr3t'

# 0: no detail, 1: detail
log_detail = 1

# Payload
payload = 0.4
###