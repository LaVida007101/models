from getEvDt import get_category
from getEvDt import summarize
from db_operations import download_upload_get_url
from identifyIfEventsV2 import return_events
from removeLinksAndHashtags import remove_links_and_hashtags
from getEvDt import get_category, get_dtls
from db_operations import initialize_db_connection
from processEvDtRes import extract_information
import unicodedata
from db_operations import write_events_to_db

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.insert(0, parent_dir)

from extractPostsFromFB import return_post_list


def normalize_unicode(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    
    ascii_text = ''.join(c for c in normalized_text if ord(c) < 128)
    
    return ascii_text

def preprocess_text(text):
    normalized_text = normalize_unicode(text)

    lower_text = normalized_text.lower()
    
    return lower_text

# extracted_posts = [
#     {
#         "time": "2024-06-02 21:00:00",
#         "post_id": "795120332725265",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid0ruSFWLpLGvsjCTDK1V3DfWTfN8HXWKNAVMF3d3KKFDrqcFESGsCTLzMYn5TtHy8fl&id=100066819165778",
#         "full_text": "📢 We've reached the end of this digital wasteland! 📢\n\nA year's worth of events and memories, will all culminate soon to top off the journey that we've had. 🚀 But beyond this point, a new horizon lies going forward, a beacon of a promising future awaits. 🌌\n\nWe are now approaching the last station ACMBlers. Please prepare as we reach the end of the line… ⚙️🌐\n\nPubmat by: Lana Huertas\nCaption by: Earl Tan\n\n#ACM2324\n#ExploringDystopiaACM\n#ACM17YSTOPIA",
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/444479311_795119666058665_580220411706088362_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=100&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_ohc=il9Enmy2XdQQ7kNvgHwBybh&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYACNVRzHVTHEzSll7opXaWEYhdDBal28wF5K0-xuns5HA&oe=66638878"
#     },
#     {
#         "time": "2024-06-01 20:36:00",
#         "post_id": "794073119496653",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid02c5J94udD1Ah2bkqqghAqMXZuLkbCwVNzTNN1hiwAKTsnmvFH45jMThTRG6sFENDml&id=100066819165778",
#         "full_text": "The battle of the bests has concluded, and what a sight to behold it was! 🌌\n\nKode Kombat: Ascension showcased the talent and skills of all participating groups. Everyone had their own tricks up their sleeve, and their game plan, and it showed. 🦾\n\nNo matter the outcome, it was one of the best competitions we’ve witnessed, and we’d like to thank all our participants for what they showed during the event! 🏁 With that concluded, Kode Kombat reaches its third and final stop, and what better way than to immortalize the memories with the pictures captured below? ✨\n\nThank you once again to all who participated, but stay tuned, as we still have more to come in the future. 🌐\n\nCaptured by: Philip Aguilar and Kendric Macaraig\nCaption by: Earl Tan\n\n#ACM2324\n#ExploringDystopiaACM\n#KodeKombatAscension",
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/444501216_794062629497702_5231948234867198425_n.jpg?stp=c120.0.480.480a_cp0_dst-jpg_e15_p480x480_q65&_nc_cat=103&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_ohc=07jAumIMlIkQ7kNvgFSoyaR&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYA5MI007FzopZ7uk_EhXOMbCoBERY2quZ81yMv4W_OJKg&oe=666363D1"
#     },
#     {
#         "time": "2024-06-01 15:47:00",
#         "post_id": "793950606175571",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid02ZtwTjBks3ERxGfakT7G9DQxBgm5UoZrpigm9zkFGoKsJetRwNterE1L1eUP51iWHl&id=100066819165778",
#         "full_text": "The results are in for Kode Kombat: Ascension! 🏆🤖 After a fierce battle through the digital landscape, we finally have our champions. Congratulations\n✨ to all the participants for their incredible efforts, and now, let's celebrate the victors!\n\n🥇 1st Place: C-Ram Productions Morayta Monsters\n🥈 2nd Place: TamaRawr\n🥉 3rd Place: SNM: KK Edition\n\nThank you to everyone who took part in this epic journey towards liberation! 🌐🦾 Until next time, keep coding and stay strong! 🚀💻\n\n#ACM2324\n#ExploringDystopiaACM\n#KodeKombatAscension\n\nCaption By: Sabrina J. Bautista\nPubmat By: Francis Chuegan\nCaptured By: Mark Robert Amor",
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/447469421_793946656175966_2507925611853240898_n.jpg?stp=cp0_dst-jpg_e15_p480x480_q65&_nc_cat=101&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_ohc=J8dNwWSL_cYQ7kNvgGANxHp&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYCqzS0Cijp9xGP6gKusBLSYFZuBDlVVv96yw6G6mDj-2g&oe=6663748D"
#     },
#     {
#         "time": "2024-05-25 15:54:00",
#         "post_id": "789815996589032",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid02vioZYh8EonEQNHvXJZGcAbfiDs76c5qy5T3rGk1ihAVpKkBpADM6gNHNiAUiY2DDl&id=100066819165778",
#         "full_text": "Race, start! 🏴🚩\n\nTeams have now begun with the fierce challenges in the digital dystopia. At last, Kode Kombat: Uprising, has officially begun! ⚔️🛡️\n\nA grueling series of games is soon to take place, and may the best team survive the last hurdle in this digital wasteland. 🌐\n\nCaptured by: Philip Aguilar\nCaption by: Earl Tan\n\n#ACM2324\n#ExploringDystopiaACM\n#KodeKombatAscension",
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/441925929_789812433256055_755330585773879564_n.jpg?stp=cp0_dst-jpg_e15_p640x640_q65&_nc_cat=103&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_ohc=y2Cw697HjX0Q7kNvgHhABpJ&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYBfUY6heMOD9wwVfbR90yRG5Tbhyo5GRQA4fs1YbDlnBQ&oe=66636E03"
#     },
#     {
#         "time": "2024-06-15 20:33:00",
#         "post_id": "802242615346370",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid0sUrw3Me5dPEGPzNPe27LTD7WmVNHUubXnzoErUojCfM2AZeVP9242oBp7zjs7BACl&id=100066819165778 ",
#         "full_text": '''It’s that time of year again, as we pass the torch to the next generation of officers that will shape our future! 🌌

# The SCC and Academic RSO Elections are almost over. We encourage all of our ACMBlers to vote and elect the upcoming leaders who will raise ACM for the next academic year 🌃🚀! You may vote for the next year’s student leaders through the link below! 🗝️

# But time is ticking! There are only a few hours left as the voting link will close by midnight! So hurry for your vote to count! 🖊️

# VOTE HERE
# https://
# forms.gle/
# nE8aUK9tJ8nvRjXU
# 8
# https://
# forms.gle/
# nE8aUK9tJ8nvRjXU
# 8
# https://
# forms.gle/
# nE8aUK9tJ8nvRjXU
# 8

# Pubmat by: Bea Ganotisi
# Caption by: Earl Tan

# #ACM2324
# #FEUTechACM
# #SCC2324
# #2425ELECTIONS''',
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/448323507_802242355346396_7418878774242918838_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=106&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_eui2=AeE262oCaNOh54aOS2QxIvjg3PPe4SZGXc_c897hJkZdz3wjDV-BlhGLjZopXwdIWR5B6z54112jN_-fee3WcFU1&_nc_ohc=Yq69qOtANTEQ7kNvgEEsDr2&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYCI9peGc3c1Nxmu86G3QYkwzoh1zER32Prlk3ZLX7_DYg&oe=66751E9B"
#     },
#     {
#         "time": "2024-06-13 15:04:00",
#         "post_id": "800921188811846",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid0QRd1XDrTtHd6TXh6Uzqmb5ZcxXmFatcoPKQCREPnLKpGDRQsXcfGV9dbahykjsxXl&id=100066819165778",
#         "full_text": '''Get ready for for a spectacular night you'll never forget.🌃🌙

# As we celebrate the culmination of FEU Tech ACM's School Year 2023-2024, let's embark on a thrilling journey through FEU Tech ACM 17STOPIAN NIGHT!🦾🌃 Create lasting memories as we entertain ourselves with fun activities, ice breakers, lively presentations, and heartfelt conversations.🫶

# Immerse yourself in an atmosphere brimming with enthusiasm and friendship as we join together to celebrate our accomplishments
# and deepen our connections. From exciting team-building exercises that encourage unity and collaboration to spontaneous moments filled with delight and laughter, 17STOPIAN NIGHT is here to help foster connections and create memorable moments.✨🎉

# Join us on this unforgettable night by registering through the links below!🚀🔗

# REGISTER NOW:
# https://bit.ly/
# ACM_17YSTOPIA_17
# YSTOPIAN_NIGHT_
# REGISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_17
# YSTOPIAN_NIGHT_
# REGISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_17
# YSTOPIAN_NIGHT_
# REGISTRATION

# Pubmat by: Bea Ganotisi
# Caption by: Ken Macaraig

# #ACM2324
# #ExploringDystop
# iaACM
# #ACM17YSTOPIA

# #ACM17thAnnivers
# ary''',
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/448314603_800913648812600_6013090100200581809_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=101&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_eui2=AeEpT3Or1nteyROh88XBtQb2Xs0Wevt0d8hezRZ6-3R3yG9hBExb4oEXhBouMNAo4bu13F9rYXVNZsbh-VBOU3Vf&_nc_ohc=sYMLPKQIfAoQ7kNvgEBhuiW&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYA-uyFNbEe3_pxJ3cneQyFciFRFLxEkt4hqrgHf04_qIw&oe=66750786"
#     },
#     {
#         "time": "2024-06-12 15:02:00",
#         "post_id": "800355512201747",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid02fAxJBJ3BSheNgbX5RWBAv64FQ1Cob7N9YkFEcuDFoFFd72hjd2Lbm8hzuZ1wLyfrl&id=100066819165778",
#         "full_text": '''Prepare for a tough battle against other competitors, as you all tackle the final leg of the digital dystopia. 🌐

# The last day will be the showdown of showdowns as brilliant minds fight against one another on the third day of ACM 17YSTOPIA, the Battle Beyond Limits. To all who want to challenge themselves, June 29, 2024, will be your shot to do so, with a Quiz Bee Competition that will surely test your limits and capabilities. 🧠⚡️

# Interested? Register now and prove you’ve got what it takes. 🔥

# REGISTER FOR DAY 3 - QUIZ BEE
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y3_QUIZBEE_REGI
# STRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y3_QUIZBEE_REGI
# STRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y3_QUIZBEE_REGI
# STRATION

# Caption By: Earl Tan
# Pubmat By: Bea Ganotisi

# #ACM2324
# #ExploringDystop
# iaACM
# #ACM17YSTOPIA
# #ACM17thAnnivers
# ary''',
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/447994560_800355295535102_5883557447580504562_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=111&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_eui2=AeEKkfC2YKWbvqOhJRX2nFVYDvVBBgLMrDYO9UEGAsysNgtgRmFbNXVO3DdFrWgBh_SF3dNDMp6p88msYKct6moa&_nc_ohc=q22S2bUkCBUQ7kNvgHk8j_K&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYCHphF6tr1vBTRqoKJe3kSiFota9vbeRI2GjRhHsWlfnQ&oe=66751DFE"
#     },
#     {
#         "time": "2024-06-11 14:24:00",
#         "post_id": "799772945593337",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid0PqmQrPtL6CD8wge46WXvYeJNyLTQYwdo2xnUQdtscqx4RL2ggAH47Q7q9FW7qpoSl&id=100066819165778",
#         "full_text": '''The future is far from now, but we must keep the strides going forward 🚀🚀.

# As we move past the digital dystopia, let's embrace our current times as we head into another era!🛸🦾. The second day of ACM 17YSTOPIA will take place on June 26, 2024, as we tackle the Journey Beyond the Tech Horizon 🌟

# This special day will deliver a panel discussion from 🧠 various special guests as we talk about:
# 📌 Navigating the Unknown: Opportunities and Challenges in Tech's Frontier

# Are you ready for the digital dystopia ahead 🌌?

# REGISTER FOR DAY 2!
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION

# Caption By: Earl Tan
# Pubmat By: Bea Ganotisi

# #ACM2324
# #ExploringDystop
# iaACM
# #ACM17YSTOPIA
# #ACM17thAnnivers
# ary''',
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/448184303_799772755593356_1503973080910725995_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=104&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_eui2=AeH5cTFe1KepjA_u2an7ui9fo95nfMD1VTqj3md8wPVVOqr3OPW8qcZLrjex10S_unZyDXyLQVVqaHjZJug0g8AG&_nc_ohc=iPDfpb6oiRYQ7kNvgEjPaM7&tn=m_kXveQ6j26tpUif&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYBSf-ySp0Ci1Odx8YW8qFTQ-TKndrUggRFgNmWB3n8WrA&oe=66750B0E"
#     },
#     {
#         "time": "2024-06-10 16:46:00",
#         "post_id": "799255255645106",
#         "post_url": "https://facebook.com/story.php?story_fbid=pfbid0ZHM2Ea8JwEKx4QkmFMrU1YuUusC57TJtVzBHAEZ13CKzXUi1fakUaoWzkEtm3wrJl&id=100066819165778",
#         "full_text": '''Time is ticking as we move headlong into the final stage of the digital wasteland.

# The first day is upon us, as ACM 17YSTOPIA sets off to venture onwards, to The Future of Tech 🌐. This June 22, 2024, prepare for informative talks as we tackle Emerging Technologies and Their Impact 🔮. Featuring talks of:

# 📌 Keynote Talk: Disruptive Innovations: Unveiling Tomorrow's Game-Changers
# 📌 Plenary Talk: Beyond the Horizon: Exploring Cutting-Edge Technologies
# 📌 Resource Talk: Transformative Trends: How Emerging Tech Reshapes Industries

# Join the kick-off of FEU Tech ACM's 17 year anniversary, and register now, for ACM 17YSTOPIA! 🚀

# REGISTER FOR DAY 1!
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION
# https://bit.ly/
# ACM_17YSTOPIA_DA
# Y1_and_DAY2_REG
# ISTRATION

# Caption By: Earl Tan
# Pubmat By: Bea Ganotisi

# #ACM2324
# #ExploringDystop
# iaACM
# #ACM17YSTOPIA
# #ACM17thAnnivers
# aryE''',
#         "image_lowquality": "https://scontent.fmnl5-2.fna.fbcdn.net/v/t39.30808-6/448207627_799255432311755_178748510803207155_n.jpg?stp=cp0_dst-jpg_e15_p843x403_q65&_nc_cat=104&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoiYiJ9&_nc_eui2=AeEeONBcZcVyJD55Hvgz_cT2TdMc5LKqUR1N0xzksqpRHcNGnqXIxxsFh4t4b8O38TepJ1TPs8yyhdYZYDZHRfoY&_nc_ohc=Ml6SvMn7itQQ7kNvgFfv-dl&_nc_ht=scontent.fmnl5-2.fna&oh=00_AYAWmx9ehaHUBDon0hQJRSVMsmP6fiXssZaYZT-UFYPj0Q&oe=6674FC53"
#     },
#     {
#         "time": "2024-06-3 13:00:00",
#         "post_id": "915068797326613",
#         "post_url": "https://www.facebook.com/photo/?fbid=915068797326613&set=a.583605170472979",
#         "full_text": '''𝗚𝗘𝗧 𝗥𝗘𝗔𝗗𝗬 𝗧𝗢 𝗕𝗘 𝗧𝗥𝗔𝗡𝗦𝗣𝗢𝗥𝗧𝗘𝗗 𝗧𝗢 𝗧𝗛𝗘 𝗙𝗔𝗥𝗧𝗛𝗘𝗦𝗧 𝗥𝗘𝗔𝗖𝗛𝗘𝗦 𝗢𝗙 𝗧𝗛𝗘 𝗚𝗔𝗟𝗔𝗫𝗬! 🌌
# Join us for 𝗜𝗧𝗔𝗠 𝗡𝗜𝗚𝗛𝗧 𝟮𝟬𝟮𝟰: 𝗧𝗛𝗥𝗢𝗨𝗚𝗛 𝗧𝗛𝗘 𝗖𝗢𝗦𝗠𝗢𝗦 on 𝗝𝗨𝗡𝗘 𝟮𝟴 at the 𝗙𝗘𝗨 𝗠𝗔𝗡𝗜𝗟𝗔 𝗚𝗥𝗔𝗡𝗗𝗦𝗧𝗔𝗡𝗗 for the biggest concert of the year! Featuring stellar performances, cosmic vibes, and a night full of music and fun. Don't miss this out-of-this-world experience!
# 🗓️ Save the date and prepare for a journey like no other. See you there, Tamaraws!
# Secure your spot now with 𝙚𝙖𝙧𝙡𝙮 𝙗𝙞𝙧𝙙 𝙧𝙚𝙜𝙞𝙨𝙩𝙧𝙖𝙩𝙞𝙤𝙣 𝙖𝙣𝙙 𝙥𝙖𝙮𝙢𝙚𝙣𝙩 at: bit.ly/IN24_EarlyBird
# Layout | Jester Sean Caspillo
# Caption | Ralph Andrei Masangkay
# #iTamNight2024
# #SCCADT2324
# #ThroughTheCosmos''',
#         "image_lowquality": "https://scontent.fceb4-1.fna.fbcdn.net/v/t39.30808-6/447443896_915055150661311_5859313947758586378_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeEQZ4BXEgoBYtFYUVHaDUfen3RpnP0OsbafdGmc_Q6xttXm-tBsRGNBbCDoowUZfYfbzRyYdoWa_nxwPkhWjEAV&_nc_ohc=Ph9H6aUAIzQQ7kNvgEekSOb&_nc_ht=scontent.fceb4-1.fna&oh=00_AYCOqNrykh7KoO_HWujr5IsgY9ELllYo7mco0TWUm781zA&oe=6678FDC3"
#     },
#     {
#         "time": "2024-06-14 15:30:00",
#         "post_id": "918744886722857",
#         "post_url": "https://www.facebook.com/photo?fbid=918744886722857&set=a.530927415504608",
#         "full_text": '''🔰 Tamaraws, are you ready to unlock the secrets behind algorithms that generate new content, such as text, images, music, or even code? 📱💻🎵🌐

# Join us on July 4 at 1:00 p.m. at the FEU Tech Innovation Center for TechX: Generative AI as we explore the future of technology, creativity, and how AI is revolutionizing industries. 🤖 Whether you're a tech enthusiast or just curious, this is the perfect opportunity to learn. Don’t miss out! 🚀

# #TechnologyDrivenByInnovation
# #TheSchoolOfInnovation
# #TechX #TechXGenerativeAI

# Pubmat: Stephen Paolo Comia (FEU Tech Innovation Center Intern) See less''',
#         "image_lowquality": "https://scontent.fceb4-1.fna.fbcdn.net/v/t39.30808-6/448277126_918728896724456_3597568211024196119_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeF1XioUUmH7lVHpnf4xFCBdEqCF9DKGfZcSoIX0MoZ9lwPBRa6B0jDNtW89m2yZkWPDFwwQxYJh8QxECyIanT-J&_nc_ohc=Eo8YMiDizzYQ7kNvgH1W9ho&_nc_ht=scontent.fceb4-1.fna&oh=00_AYDqlhyc2zekgG0rRIMA784nJ6txEyLSo6VHO7TZYXvgOA&oe=66791C90"
#     }
# ]

extracted_posts = return_post_list()

initialize_db_connection()
events_lists = return_events(extracted_posts)

events_with_categories = [{preprocess_text(remove_links_and_hashtags(item["full_text"])):get_category(remove_links_and_hashtags(preprocess_text(item["full_text"])))} for item in events_lists]

events_with_details = [extract_information(get_dtls(item["full_text"])) for item in events_lists]


event_profiles = []

for raw_data, events_with_cat, event_details in zip(events_lists, events_with_categories, events_with_details):
    full_text, category = next(iter(events_with_cat.items()))
    new_dictionary = {
        "details":{
            "id"            : raw_data["post_id"],
            "category"      : category,
            "date"          : event_details[1],
            "description"   : summarize(full_text),
            "image_link"    : download_upload_get_url(raw_data["image_lowquality"], raw_data["post_id"]),
            "link"          : raw_data["post_url"],
            "location"      : "Location: TBA" if event_details[2] is None or event_details[2] == "None" else event_details[2],
            "name"          : event_details[0]
        },
        "id": raw_data["post_id"]
    }

    event_profiles.append(new_dictionary)



event_profiles = [event for event in event_profiles if not (event["details"]["date"] == "None" and event["details"]["location"] == "Location: TBA")]


for event in event_profiles:
    print(event, "\n\n\n")
# write_events_to_db(event_profiles)


