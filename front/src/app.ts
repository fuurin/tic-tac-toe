/// <reference path="../node_modules/phaser/types/phaser.d.ts"/>
import "phaser"
import { MainScene } from "./mainScene";
 
const config: Phaser.Types.Core.GameConfig = {
    title: "AI tic-tac-toe",
    width: 600,
    height: 800,
    parent: "app",
    scene: [MainScene],
    backgroundColor: "#cccccc"
}

export class TTTGame extends Phaser.Game {
    constructor(config: Phaser.Types.Core.GameConfig) {
        super(config)
    }
}

window.onload = () => {
    new TTTGame(config);
}