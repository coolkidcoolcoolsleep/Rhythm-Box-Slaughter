import time
from ball_tracking
from random_rythm_box


# 점수 계산
# 1. 랜덤좌표 끌고오고
# 2. 인식된 자표 끌고와서
# 3. 비교
# 4. 점수를 부여
# 5. 총합산
# 6. 위너(2P)

# 랜덤하게 생성된 좌표와 tracking 돼서 나온 좌표값이 일치할 때 + 10
# 랜덤하게 생성된 좌표에 tracking 돼서 나온 좌표값이 일치하지 않을 때 -1



class Score:

    def showOnePlayerGameStats(self, elapsedTime, maxRep, currentRep):
        widthPositionFactor = 3
        textColor = (114, 70, 20)
        titleScale = 1
        titleThickness = 3
        valueScale = 1.5
        valueThickness = 4

        progTitle = 'SCORE'
        progTitleTopPad = 10
        progValueTopPad = progTitleTopPad + 15
        progValue = str(currentRep) + '/' + str(maxRep)
        progTitleX, progTitleY, _, progTitleHeight = self.getTextPosition(progTitle, self.defaultFont, titleScale,
                                                                          titleThickness, widthPositionFactor,
                                                                          widthPos='right', heightPos='top')
        progValueX, progValueY, _, _ = self.getTextPosition(progValue, self.defaultFont, valueScale, valueThickness,
                                                            widthPositionFactor, widthPos='right', heightPos='top')
        self.videoManager.addText(progTitle, (progTitleX, progTitleY + progTitleTopPad), self.defaultFont, titleScale,
                                  textColor, titleThickness)
        self.videoManager.addText(progValue, (progValueX, progValueY + progTitleHeight + progValueTopPad), self.defaultFont,
                                  valueScale, textColor, valueThickness)

        if self.player1.freezeRoundResult:
            self.addText(timeValue, textScale=4, textThickness=8)


    def showTwoPlayerGameStats(self, elapsedTime, maxReps, currentReps):
        widthPositionFactor = 4
        textColor = (114, 70, 20)
        timeTitleScale = 2
        timeTitleThickness = 5
        timeValueScale = 3
        timeValueThickness = 8
        progTitleScale = 1
        progTitleThickness = 3
        progValueScale = 1.5
        progValueThickness = 4

        progTitle = 'PROGRESS'
        progTitleTopPad = 10
        progValueTopPad = progTitleTopPad + 15

        progValueP1 = str(currentReps[0]) + '/' + str(maxReps[0])
        progTitleP1X, progTitleP1Y, _, progTitleP1Height = self.getTextPosition(progTitle, self.defaultFont, progTitleScale,
                                                                                progTitleThickness, widthPositionFactor,
                                                                                heightPos='top')
        progValueP1X, progValueP1Y, _, _ = self.getTextPosition(progValueP1, self.defaultFont, progValueScale,
                                                                progValueThickness, widthPositionFactor, heightPos='top')
        self.videoManager.addText(progTitle, (progTitleP1X, progTitleP1Y + progTitleTopPad), self.defaultFont,
                                  progTitleScale, textColor, progTitleThickness)
        self.videoManager.addText(progValueP1, (progValueP1X, progValueP1Y + progTitleP1Height + progValueTopPad),
                                  self.defaultFont, progValueScale, textColor, progValueThickness)

        progValueP2 = str(currentReps[1]) + '/' + str(maxReps[1])
        progTitleP2X, progTitleP2Y, _, progTitleP2Height = self.getTextPosition(progTitle, self.defaultFont, progTitleScale,
                                                                                progTitleThickness, widthPositionFactor,
                                                                                widthPos='right', heightPos='top')
        progValueP2X, progValueP2Y, _, _ = self.getTextPosition(progValueP2, self.defaultFont, progValueScale,
                                                                progValueThickness, widthPositionFactor, widthPos='right',
                                                                heightPos='top')
        self.videoManager.addText(progTitle, (progTitleP2X, progTitleP2Y + progTitleTopPad), self.defaultFont,
                                  progTitleScale, textColor, progTitleThickness)
        self.videoManager.addText(progValueP2, (progValueP2X, progValueP2Y + progTitleP2Height + progValueTopPad),
                                  self.defaultFont, progValueScale, textColor, progValueThickness)

        splitLine1Pt1 = (int(self.videoManager.frameWidth / 2), 0)
        splitLine1Pt2 = (int(self.videoManager.frameWidth / 2), timeTitleY - timeTitleHeight - 5)
        splitLine2Pt1 = (int(self.videoManager.frameWidth / 2), timeValueY + timeValueHeight + 30)
        splitLine2Pt2 = (int(self.videoManager.frameWidth / 2), int(self.videoManager.frameHeight))
        self.videoManager.addLine(splitLine1Pt1, splitLine1Pt2, (255, 255, 255), thickness=self.twoPlayerSplitLineThickness)
        self.videoManager.addLine(splitLine2Pt1, splitLine2Pt2, (255, 255, 255), thickness=self.twoPlayerSplitLineThickness)


        # 우승자 표시
        winnerText = 'WINNER'
        if self.player1.freezeRoundResult:
            self.addText(winnerText, textScale=3, textThickness=6, widthFactor=2)
        elif self.player2.freezeRoundResult:
            self.addText(winnerText, textScale=3, textThickness=6, widthFactor=2, widthPos='right')




