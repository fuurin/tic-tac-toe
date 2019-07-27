import "phaser"
import { TTT } from "./ttt";

const BASE_TTT_URL: string = "http://127.0.0.1:5000";
const BOX_SIZE: number = 130;

export class MainScene extends Phaser.Scene {
    private boxes: Phaser.GameObjects.Rectangle[][];
    private board: string[][];
    private ttt: TTT;

    constructor() {
        super({ key: "MainScene" });
    }
    
    init(params: any) {
        this.board = [
            ['+', '+', '+'],
            ['+', '+', '+'],
            ['+', '+', '+']
        ]
        this.ttt = new TTT(BASE_TTT_URL);
    }
    
    preload() {}

    create() {
        this.createTitle();
        this.createResetButton();
        this.boxes = this.createBoxes();
    }

    update(time: number) {}

    private createBoxes(): Phaser.GameObjects.Rectangle[][] {
        const diff = this.game.canvas.height - this.game.canvas.width;
        const offsetX = (this.game.canvas.width - (BOX_SIZE * 2)) / 2;
        const offsetY = diff + (this.game.canvas.width - (BOX_SIZE * 2)) / 2;
        
        const boxes: Phaser.GameObjects.Rectangle[][] = [];
        for (let j = 0; j < 3; j++) {
            const row: Phaser.GameObjects.Rectangle[] = [];
            for (let i = 0; i < 3; i++) {
                const x: number = offsetX + BOX_SIZE * i;
                const y: number = offsetY + BOX_SIZE * j;
                const box = this.createBox(x, y);
                row.push(box);
                box.setInteractive();
                box.on('pointerdown', this.move(j, i), this);
            }
            boxes.push(row);
        }

        return boxes;
    }

    private createTitle(): Phaser.GameObjects.Text {
        const style = { font: '64px Ariel Bold', fill: 0xfbfbac };
        const title = this.add.text(300, 80, "AI 三目並べ", style);
        title.setOrigin(0.5, 0.5);
        return title
    }

    private createResetButton(): Phaser.GameObjects.Rectangle {
        const resetButton = this.add.rectangle(300, 200, 250, 80, 0xaaaaaa);
        resetButton.setStrokeStyle(5, 0x111111);
        resetButton.setInteractive();
        resetButton.on('pointerdown', () => {this.scene.start("MainScene")}, this);
        
        const style = { font: '32px Ariel Bold', fill: 0x11111 };
        const resetButtonText = this.add.text(300, 200, "最初から", style)
        resetButtonText.setOrigin(0.5, 0.5);
        
        return resetButton;
    }

    private createBox(x: number, y: number): Phaser.GameObjects.Rectangle {
        const rect = this.add.rectangle(x, y, BOX_SIZE, BOX_SIZE, 0xfbfbac);
        rect.setStrokeStyle(5, 0x111111);
        return rect;
    }

    private createStone(row: number, col: number, isPlayer: boolean = true): Phaser.GameObjects.Arc {
        const color = isPlayer ? 0x333333 : 0xeeeeee;
        const box: Phaser.GameObjects.Rectangle = this.boxes[row][col]
        const stone = this.add.circle(box.x+30, box.y+30, (BOX_SIZE - 10) / 2, color); // 謎の30ズレ
        stone.setStrokeStyle(3, 0x000000);
        this.board[row][col] = isPlayer ? 'x' : 'o';
        return stone;
    }

    private move(row: number, col: number): () => void {
        return () => {
            this.playerMove(row, col);
            this.enemyMove(this.board);
        }
    }

    private playerMove(row: number, col: number) {
        const box = this.boxes[row][col];
        this.createStone(row, col);
        box.removeInteractive();
    }

    private enemyMove(board: string[][]) {
        this.ttt.bot(board, (data: any) => {
            console.log(data);
            const row: number = data['response']['row'] - 1;
            const col: number = data['response']['col'] - 1;
            this.createStone(row, col, false);
            this.boxes[row][col].removeInteractive();
        });
    }
}