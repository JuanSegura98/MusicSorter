# The purpose of this program is to sort a bunch of songs with typical formats in folders.
# Change the global variable MUSIC_DIRECTORY to your Music path WITH / AT THE END

# Admitted formats are:
#   Author - Song name
#   Song name - Author
#   Song name

from os import popen
from os import system
from getkey import getkey, keys

# GLOBAL VARIABLES
MUSIC_DIRECTORY = '/home/juans/Music/'


def choosingMenu(enterList, header='Select an option:'):
    """
    :argument: list of options to display, optional heading
    :return: chosen option

    """
    chosen = 0
    key = '\0'
    system('clear')
    while key != '\n':
        print(header)

        for element in enterList:
            if element == enterList[chosen]:  # Outputs chosen object with the format
                print("\033[7m" + element + "\033[27m")
            else:
                print(element)

        key = getkey()
        if key == keys.DOWN and chosen < len(enterList) - 1:
            chosen += 1
        if key == keys.UP and chosen > 0:
            chosen -= 1

        system('clear')

    return enterList[chosen]


def checkMusicDirectory():
    """
    :argument: none
    :return: List of the songs and list of the folders

    """

    songString = popen('ls {}'.format(MUSIC_DIRECTORY)).read()
    fileList = songString.split('\n')  # We save every entry in a list
    fileList.pop(len(fileList) - 1)  # The last entry is a blank
    songList = []
    folderList = []

    for file in fileList:
        if file.endswith('.mp3'):
            songList.append(file)
        else:
            folderList.append(file)
    return songList, folderList


def checkSongs(songs, folders):
    for song in songs:
        author_song = song.split('-')
        if len(author_song) > 1:  # SOMETHING - SOMETHING
            author_song[0] = author_song[0].strip()  # Erase leading and trailing whitespaces
            author_song[1] = author_song[1][:-4]  # Remove .mp3
            author_song[1] = author_song[1].strip()

            if author_song[0] in folders:  # The Author already has a folder
                system('mv "' + MUSIC_DIRECTORY + song + '" ' + '"' + MUSIC_DIRECTORY + author_song[0] + '" 2>/dev/null')
            elif author_song[1] in folders:  # The Author already has a folder and the name is reversed
                system('mv "' + MUSIC_DIRECTORY + song + '" ' + '"' + MUSIC_DIRECTORY + author_song[1] + '/' + author_song[1] + " - " + author_song[0] + '.mp3" 2>/dev/null')
            else:  # There is no folder yet
                key = input("There is no folder yet for {}. Create folder \033[1m{}\033[0m? (y)".format(song, author_song[0]))  # Create folder if it does not exist
                if key == "" or key == "y" or key == "Y":
                    system('mkdir ' + "'" + MUSIC_DIRECTORY + author_song[0] + "'")
                    songs, folders = checkMusicDirectory()
                    checkSongs(songs, folders)
                else:
                    songOptions = ['Choose existing folder', 'Rename file', 'Skip ', 'Quit']
                    chosenOption = choosingMenu(songOptions)
                    if chosenOption == songOptions[0]:  # Choose existing folder and move the current song to the chosen folder
                        folders_and_quit = folders
                        folders_and_quit.append('Quit')
                        chosenDirectory = choosingMenu(folders_and_quit, 'Select folder:')
                        if chosenDirectory == 'Quit':
                            songs, folders = checkMusicDirectory()
                            checkSongs(songs, folders)
                        else:
                            system('mv "' + MUSIC_DIRECTORY + song + '" ' + '"' + MUSIC_DIRECTORY + chosenDirectory + '" 2>/dev/null')
                    elif chosenOption == songOptions[1]:  # Rename the file
                        print('Current song: \033[1m' + song + '\033[0m')
                        newname = input("Enter new file name (Artist - song). Enter Q to cancel: ")
                        if newname == 'Q' or newname == 'q':
                            songs, folders = checkMusicDirectory()
                            checkSongs(songs, folders)
                        elif newname.endswith('.mp3'):
                            system('mv "' + MUSIC_DIRECTORY + song + '" ' + '"' + MUSIC_DIRECTORY + newname + '" 2>/dev/null')
                            songs[songs.index(song)] = newname
                        else:
                            system('mv "' + MUSIC_DIRECTORY + song + '" ' + '"' + MUSIC_DIRECTORY + newname + '.mp3" 2>/dev/null')
                        songs, folders = checkMusicDirectory()
                        checkSongs(songs, folders)
                    elif chosenOption == songOptions[2]:    # Skip -> Next iteration. Remove from list
                        pass
                    elif chosenOption == songOptions[3]:    # Terminate program
                        quit()

        else:  # SONG NAME, WITHOUT -
            print('The song needs a rename')
            print('Current song: \033[1m' + song + '\033[0m')
            newname = input("Enter new file name (Artist - song). Enter Q to cancel: ")
            if newname == 'Q' or newname == 'q':
                songs, folders = checkMusicDirectory()
                checkSongs(songs, folders)
            elif newname.endswith('.mp3'):
                system("mv '" + MUSIC_DIRECTORY + song + "' " + "'" + MUSIC_DIRECTORY + newname + "' 2>/dev/null")
                songs[songs.index(song)] = newname
            else:
                system("mv '" + MUSIC_DIRECTORY + song + "' " + "'" + MUSIC_DIRECTORY + newname + ".mp3' 2>/dev/null")
                songs[songs.index(song)] = newname + '.mp3'
            songs, folders = checkMusicDirectory()
            checkSongs(songs, folders)

        songs, folders = checkMusicDirectory()  # Recheck what we have


songs, folders = checkMusicDirectory()
checkSongs(songs, folders)
print('Done!')
