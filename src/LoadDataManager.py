import pygame
import json
import os
from Settings import *

class LoadDataManager:
    def __init__(self):
        #File Names for storing different parts of the game.
        self.SettingsFileName='Settings.json'
        self.PlayerFileName='Player.json'
        self.EnemySpritesFileName='Enemies.json'
        self.LootSpritesFileName='loots.json'
        self.GameFileName='game.json'
        self.LevelFolderName='levels'

    def SaveTheLevels(self,dir_path,levels):
        #Make the Levels directory.
        if(os.path.exists(os.path.join(dir_path,self.LevelFolderName))):
            pass
        else:
            os.mkdir(os.path.join(dir_path,self.LevelFolderName))

        for level in levels:
            filePath=os.path.join(dir_path,self.LevelFolderName,f'{level["level_id"]}.json')
            with open(filePath, 'w') as f:
                json.dump(level,f)

    def createSaveGameDirectory(self,folderName):
        #Make a directory with player Name, age as the folder name.
        dir_path=os.path.join(os.getcwd(),"SAVED_GAMES",folderName)
        if(os.path.exists(dir_path)):
            pass
        else:
            os.mkdir(dir_path)
        pass

    def saveDialogLogs(self, DIALOG_LOGS,folderName):
        filePath=os.path.join(os.getcwd(), "SAVED_GAMES",folderName, f'DIALOG_LOGS.json')
        with open(filePath,'w') as f:
            json.dump(DIALOG_LOGS,f)
        pass

    def saveTheGame(self,gameData,folderName):
        dir_path=os.path.join(os.getcwd(),"SAVED_GAMES",folderName)

        #Make separate files for different things and write appropriate data. For levels, have to create files inside the folder named 'levels'
            #Writing the settings data.
        with open(os.path.join(dir_path,self.SettingsFileName), 'w') as f:
            json.dump(gameData['GameSettings'],f)    
        del gameData['GameSettings']

            #Writing the player data.
        with open(os.path.join(dir_path,self.PlayerFileName),'w') as f:
            json.dump(gameData['player'],f)
        del gameData['player']

            #Writing the levels.
        self.SaveTheLevels(dir_path,gameData['levels'])
        del gameData['levels']

            #Writing the rest of the game.
        with open(os.path.join(dir_path,self.GameFileName),'w') as f:
            json.dump(gameData,f)
            
    #A method to display the saved games, shows the Name, age values only.
    def savedGamesInfo(self):
        dirPath=os.path.join(os.getcwd(),"SAVED_GAMES")
        fileNames=os.listdir(dirPath)

        savedGames=[]
        for fileName in fileNames:
            savedGame=fileName.split('_',2)
            savedGames.append(savedGame)
        return savedGames