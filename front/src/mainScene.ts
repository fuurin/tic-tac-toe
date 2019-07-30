import "phaser"
import { TTT } from "./ttt";

// const BASE_TTT_URL: string = "https://tic-tac-toe-minimax-bot.herokuapp.com/";
const BASE_TTT_URL: string = "http://127.0.0.1:5000";
const BOX_SIZE: number = 130;

export class MainScene extends Phaser.Scene {
    private messageText: Phaser.GameObjects.Text;
    private first: string;
    private boxes: Phaser.GameObjects.Rectangle[][];
    private board: string[][];
    private ttt: TTT;
    private color = {
        'x': "#222222",
        'o': "#fbfbfb",
        "draw": "#bbbbbb",
    }

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
        this.first = params["first"] || "x";
    }

    create() {
        this.messageText = this.createTitle();
        this.createBlackStartButton();
        this.createWhiteStartButton();
        this.boxes = this.createBoxes();

        if (this.first === "o") {
            this.enemyMove(this.board);
        }
    }

    private createTitle(): Phaser.GameObjects.Text {
        const style = { font: '64px Ariel Bold', fill: 0xfbfbac };
        const title = this.add.text(300, 80, "AI 三目並べ", style);
        title.setOrigin(0.5, 0.5);
        return title
    }

    private createBlackStartButton(): Phaser.GameObjects.Group {
        const button = this.add.rectangle(180, 200, 200, 80, 0x999999);
        button.setStrokeStyle(3);
        // const text = "最初から";
        const text = "黒から";
        const textStyle = { font: '32px Ariel Bold', fill: 0x111111 };
        return this.createButton(() => { 
            this.scene.start("MainScene", {first: "x"});
        }, button, text, textStyle)
    }

    private createWhiteStartButton(): Phaser.GameObjects.Group {
        const button = this.add.rectangle(420, 200, 200, 80, 0xfbfbfb);
        button.setStrokeStyle(3);
        const text = "白から"
        const textStyle = { font: '32px Ariel Bold', fill: 0x111111 };
        return this.createButton(() => { 
            this.scene.start("MainScene", {first: "o"});
        }, button, text, textStyle)
    }

    private createButton(callback: () => void, shape: Phaser.GameObjects.Shape, text: string, textStyle?: any): Phaser.GameObjects.Group {
        shape.setInteractive();
        shape.on('pointerdown', callback, this);
        const buttonText = this.add.text(shape.x, shape.y, text, textStyle);
        buttonText.setOrigin(0.5, 0.5);
        return new Phaser.GameObjects.Group(this, [shape, buttonText]);
    }

    private createBox(x: number, y: number): Phaser.GameObjects.Rectangle {
        const rect = this.add.rectangle(x, y, BOX_SIZE, BOX_SIZE, 0xfbfbac);
        rect.setStrokeStyle(5, 0x111111);
        return rect;
    }

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
        this.createStone(row, col, true);
        box.removeInteractive();
    }

    private enemyMove(board: string[][]) {
        this.scene.pause();
        this.message("白が考え中…", this.color.o);
        this.ttt.bot(board, (data: any) => {
            this.scene.resume();

            if (data["winner"] === null || data["winner"] === "o") {
                const row: number = data['response']['row'];
                const col: number = data['response']['col'];
                this.createStone(row, col, false);
                this.boxes[row][col].removeInteractive();
            }
            
            if (data["winner"] !== null) {
                this.finish(data["winner"]);
            } else {
                this.message("黒の番です", this.color.x)
            }
        });
    }

    private finish(winner: string) {
        const result: any = {
            "x": ["黒の勝ち！", this.color.x],
            "o": ["白の勝ち！", this.color.o],
            "draw": ["引き分け！", this.color.draw]
        }
        this.message(result[winner][0], result[winner][1])
        this.boxes.forEach((row) => {
            row.forEach((box) => {
                box.disableInteractive();
            });
        });
        return
    }

    private message(text: string, color: string) {
        this.messageText.setText(text);
        const style = { font: '64px Ariel Bold', fill: color }
        this.messageText.setStyle(style);
        this.messageText.setStroke("#111111", 3);
    }
}