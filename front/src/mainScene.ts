import "phaser"

const BOX_SIZE: number = 130;

export class MainScene extends Phaser.Scene {
    
    private isPlayer: boolean = true;

    constructor() {
        super({
            key: "MainScene"
        });
    }
    
    init(params: any) {
        
    }
    
    preload() {}

    create() {
        this.createTitle();
        this.createResetButton();
        this.createBoxes();
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
                box.setInteractive();
                box.on('pointerdown', this.move(box, j, i), this);
                row.push(box);
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

    private createStone(x: number, y: number, isPlayer: boolean = true): Phaser.GameObjects.Arc {
        const color = isPlayer ? 0x333333 : 0xeeeeee;
        const stone = this.add.circle(x+30, y+30, (BOX_SIZE - 10) / 2, color); // 謎の30ズレ
        stone.setStrokeStyle(3, 0x000000);
        return stone;
    }

    private move(box: Phaser.GameObjects.Rectangle, row: number, col: number): () => void {
        return () => {
            this.createStone(box.x, box.y, this.isPlayer);
            box.removeInteractive();
            this.isPlayer = !this.isPlayer;
        }
    }
}