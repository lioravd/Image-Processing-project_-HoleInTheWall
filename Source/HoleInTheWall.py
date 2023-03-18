import pygame
import pygame.camera
import random
from Source.figureMatching import PointsGrading, MarkMistake
from Utils import utilities as utl
import moviepy.editor as mp


class HoleInTheWallGame:
    def __init__(self):
        self.scoreTable = [('Default Player 1', 0),
                           ('Default Player 2', 0),
                           ('Default Player 3', 0)]

        self.minScore, self.maxScore = -100, 100
        self.maxLimitToNextLevel = 5
        self.PHOTO_EXPIRE_TIME = 1000*30    # 30 sec until next calibration image

        self.levelSpeed = \
            {
                1:  # easy
                    {
                        "dx": 0,
                        "dy": 1/10,
                        "dw": 1.0,
                        "dh": 1.0
                    },
                2:  # mid
                    {
                        "dx": 0,
                        "dy": 1/10,
                        "dw": 1.2,
                        "dh": 1.2
                    },
                3:  # hard
                    {
                        "dx": 0,
                        "dy": 1/10,
                        "dw": 1.4,
                        "dh": 1.4
                    }
            }

        self.trailerPath = []
        self.screen = None
        self.calibration_image = None
        self.cam = None
        self.camera_surface = None
        self.clock = None
        self.currentPlayer = None
        self.sound_passWall = None
        self.sound_crashWall = None

        self.paths = \
            {
                "wallBackground": "../img/brick-wall.jpg",
                "wallsImages":
                    {
                        1:  # one player
                            {
                                1: "../walls/onePlayer/easy",
                                2: "../walls/onePlayer/mid",
                                3: "../walls/onePlayer/hard"
                            },
                        2:  # two players
                            {
                                1: "../walls/twoPlayer/easy",
                                2: "../walls/twoPlayer/mid",
                                3: "../walls/twoPlayer/hard"
                            }
                    }
            }

        self.addedScore = None
        self.addedScore_pos = None
        self.addedScore_alpha = 0
        self.addedScore_speed = 0

        # ~~~~ Init pygame
        pygame.init()
        pygame.display.set_caption("Hole In The Wall")

        #~~~~ Init sound tracks
        self.sound_passWall = pygame.mixer.Sound("../sounds/mixkit-arcade-bonus-alert-767.wav")
        self.sound_crashWall = pygame.mixer.Sound("../sounds/mixkit-losing-drums-2023.wav")
        self.sound_background = pygame.mixer.Sound("../sounds/disco-funk-loops.mp3")
        self.game_background = pygame.mixer.Sound("../sounds/game_music.wav")


        # ~~~~ Init clock
        self.clock = pygame.time.Clock()

        # ~~~~~ Init screen
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height)) # , pygame.FULLSCREEN)

        # ~~~~ Init the camera
        pygame.camera.init()
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[1])
        self.cam.set_controls(hflip=True, vflip=False)  # Set the camera controls to flip the image
        self.cam.start()
        self.camera_surface = pygame.Surface((screen_width, screen_height))  # Create a surface for the camera video

        #~~~~ Init Trailer movie
        self.trailer_movie = mp.VideoFileClip("../video/tmp.mp4")
        self.trailer_movie_sound = pygame.mixer.Sound("../video/tmp.wav")

    def Run(self):
        from Source.HomePage import main_menu
        main_menu(self)

    def insertPlayerScore(self):
        self.scoreTable.append((self.currentPlayer.name, self.currentPlayer.score))

    def passWallRecognition(self, frame, wall_mask, BB):
        calibration_image = self.currentPlayer.calibration_image
        score = PointsGrading(wall_mask, frame, calibration_image, BB)

        self.addedScore_alpha = 255
        self.addedScore_speed = 3

        if (score == 0):
            self.addedScore = utl.get_font(80).render(f"-1", True, "#FF1E1E")
            self.addedScore_pos = (self.screen.get_width() - self.addedScore.get_width() // 2-60, 10 + self.addedScore.get_height() // 2)
            # add faile animation
            c_list = MarkMistake()
            for circle in c_list:
                pygame.draw.circle(self.screen, (207, 0, 0, 255), circle[0], circle[1]+5)
                pygame.draw.circle(self.screen, (59, 0, 0, 128), circle[0], circle[1])
                pygame.display.update()
            pygame.time.wait(2000)
            self.sound_crashWall.play()
            self.currentPlayer.life -= 1
        else:
            self.addedScore = utl.get_font(80).render(f"+{score}", True, "#865DFF")
            self.addedScore_pos = (self.addedScore.get_width() // 2, 10 + self.addedScore.get_height() // 2)
            # add success animation
            self.sound_passWall.play()
            self.currentPlayer.counter_success += 1
        self.currentPlayer.score += score

        return score

    def captureCalibrationImage(self, frame):
        self.calibration_image = frame
