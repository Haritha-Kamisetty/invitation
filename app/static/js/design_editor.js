// Design Editor - Canva-like functionality
// Comprehensive design tool with text, shapes, drawing, colors, and layers

let canvas;
let currentTool = 'select';
let drawingMode = false;
let history = [];
let historyStep = 0;
let selectedObject = null;

// Initialize Canvas
document.addEventListener('DOMContentLoaded', function () {
    initializeCanvas();
    setupEventListeners();
});

function initializeCanvas() {
    canvas = new fabric.Canvas('design-canvas', {
        width: 800,
        height: 600,
        backgroundColor: '#ffffff',
        preserveObjectStacking: true
    });

    // Selection events
    canvas.on('selection:created', handleSelection);
    canvas.on('selection:updated', handleSelection);
    canvas.on('selection:cleared', clearSelection);
    canvas.on('object:modified', saveState);
    canvas.on('object:added', saveState);
    canvas.on('object:removed', saveState);

    // Initial state
    saveState();
}

function setupEventListeners() {
    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
        // Ctrl+Z - Undo
        if (e.ctrlKey && e.key === 'z') {
            e.preventDefault();
            undoAction();
        }
        // Ctrl+Y - Redo
        if (e.ctrlKey && e.key === 'y') {
            e.preventDefault();
            redoAction();
        }
        // Delete - Remove selected
        if (e.key === 'Delete' || e.key === 'Backspace') {
            const activeObject = canvas.getActiveObject();
            // Only delete if NOT editing text
            if (activeObject && !activeObject.isEditing) {
                e.preventDefault(); // Prevent browser back navigation
                deleteSelected();
            }
        }
        // Ctrl+C - Copy
        if (e.ctrlKey && e.key === 'c') {
            copySelected();
        }
        // Ctrl+V - Paste
        if (e.ctrlKey && e.key === 'v') {
            pasteSelected();
        }
    });
}

// ==================== TOOL SELECTION ====================

function selectTool(tool) {
    currentTool = tool;

    // Update active button
    document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tool="${tool}"]`).classList.add('active');

    // Disable drawing mode
    canvas.isDrawingMode = false;

    // Load tool panel
    loadToolPanel(tool);
}

function loadToolPanel(tool) {
    const panel = document.getElementById('tool-panel');

    switch (tool) {
        case 'text':
            panel.innerHTML = getTextPanel();
            break;
        case 'shapes':
            panel.innerHTML = getShapesPanel();
            break;
        case 'draw':
            panel.innerHTML = getDrawPanel();
            break;
        case 'image':
            panel.innerHTML = getImagePanel();
            break;
        case 'background':
            panel.innerHTML = getBackgroundPanel();
            break;
        case 'layers':
            panel.innerHTML = getLayersPanel();
            updateLayersList();
            break;
        default:
            panel.innerHTML = `
                <div class="panel-section">
                    <div class="panel-title">Select Tool</div>
                    <p style="color: #666; font-size: 14px;">
                        Click on objects to select and modify them.
                    </p>
                </div>
            `;
    }
}

// ==================== TEXT TOOLS ====================

function getTextPanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Add Text</div>
            <button class="toolbar-btn" onclick="addText('heading')" style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-heading"></i> Add Heading
            </button>
            <button class="toolbar-btn" onclick="addText('subheading')" style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-text-height"></i> Add Subheading
            </button>
            <button class="toolbar-btn" onclick="addText('body')" style="width: 100%;">
                <i class="fas fa-paragraph"></i> Add Body Text
            </button>
        </div>

        <div class="panel-section">
            <div class="panel-title">Font Family</div>
            <div class="font-grid">
                <div class="font-option" style="font-family: 'Playfair Display', serif;" onclick="changeFont('Playfair Display')">
                    Playfair Display
                </div>
                <div class="font-option" style="font-family: 'Montserrat', sans-serif;" onclick="changeFont('Montserrat')">
                    Montserrat
                </div>
                <div class="font-option" style="font-family: 'Roboto', sans-serif;" onclick="changeFont('Roboto')">
                    Roboto
                </div>
                <div class="font-option" style="font-family: 'Open Sans', sans-serif;" onclick="changeFont('Open Sans')">
                    Open Sans
                </div>
                <div class="font-option" style="font-family: 'Lato', sans-serif;" onclick="changeFont('Lato')">
                    Lato
                </div>
                <div class="font-option" style="font-family: 'Poppins', sans-serif;" onclick="changeFont('Poppins')">
                    Poppins
                </div>
                <div class="font-option" style="font-family: 'Dancing Script', cursive;" onclick="changeFont('Dancing Script')">
                    Dancing Script
                </div>
                <div class="font-option" style="font-family: 'Pacifico', cursive;" onclick="changeFont('Pacifico')">
                    Pacifico
                </div>
                <div class="font-option" style="font-family: 'Lobster', cursive;" onclick="changeFont('Lobster')">
                    Lobster
                </div>
                <div class="font-option" style="font-family: 'Great Vibes', cursive;" onclick="changeFont('Great Vibes')">
                    Great Vibes
                </div>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Text Colors</div>
            <div class="color-grid">
                ${generateColorSwatches('text')}
            </div>
            <div class="color-picker-wrapper" style="margin-top: 10px;">
                <div class="color-picker-btn">
                    <input type="color" id="text-color-picker" onchange="changeTextColor(this.value)">
                    <span style="padding: 10px;">Custom Color</span>
                </div>
            </div>
        </div>
    `;
}

function addText(type) {
    let text, fontSize, fontWeight;

    switch (type) {
        case 'heading':
            text = 'Add Heading';
            fontSize = 48;
            fontWeight = 'bold';
            break;
        case 'subheading':
            text = 'Add Subheading';
            fontSize = 32;
            fontWeight = '600';
            break;
        default:
            text = 'Add body text';
            fontSize = 18;
            fontWeight = 'normal';
    }

    const textObj = new fabric.IText(text, {
        left: canvas.width / 2,
        top: canvas.height / 2,
        fontSize: fontSize,
        fontWeight: fontWeight,
        fontFamily: 'Montserrat',
        fill: '#000000',
        originX: 'center',
        originY: 'center'
    });

    canvas.add(textObj);
    canvas.setActiveObject(textObj);
    canvas.renderAll();
}

function changeFont(fontFamily) {
    const activeObject = canvas.getActiveObject();
    if (activeObject && activeObject.type === 'i-text') {
        activeObject.set('fontFamily', fontFamily);
        canvas.renderAll();
    }
}

function changeTextColor(color) {
    const activeObject = canvas.getActiveObject();
    if (activeObject && (activeObject.type === 'i-text' || activeObject.type === 'text')) {
        activeObject.set('fill', color);
        canvas.renderAll();
    }
}

// ==================== SHAPES TOOLS ====================

function getShapesPanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Basic Shapes</div>
            <div class="shape-grid">
                <button class="shape-btn" onclick="addShape('rectangle')" title="Rectangle">
                    <i class="far fa-square"></i>
                </button>
                <button class="shape-btn" onclick="addShape('circle')" title="Circle">
                    <i class="far fa-circle"></i>
                </button>
                <button class="shape-btn" onclick="addShape('triangle')" title="Triangle">
                    <i class="fas fa-play" style="transform: rotate(-90deg);"></i>
                </button>
                <button class="shape-btn" onclick="addShape('line')" title="Line">
                    <i class="fas fa-minus"></i>
                </button>
                <button class="shape-btn" onclick="addShape('arrow')" title="Arrow">
                    <i class="fas fa-arrow-right"></i>
                </button>
                <button class="shape-btn" onclick="addShape('star')" title="Star">
                    <i class="fas fa-star"></i>
                </button>
                <button class="shape-btn" onclick="addShape('heart')" title="Heart">
                    <i class="fas fa-heart"></i>
                </button>
                <button class="shape-btn" onclick="addShape('polygon')" title="Hexagon">
                    <i class="fas fa-stop"></i>
                </button>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Fill Colors</div>
            <div class="color-grid">
                ${generateColorSwatches('fill')}
            </div>
            <div class="color-picker-wrapper" style="margin-top: 10px;">
                <div class="color-picker-btn">
                    <input type="color" id="fill-color-picker" onchange="changeFillColor(this.value)">
                    <span style="padding: 10px;">Custom Color</span>
                </div>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Stroke</div>
            <div class="color-grid">
                ${generateColorSwatches('stroke')}
            </div>
            <div style="margin-top: 10px;">
                <label class="property-label">Stroke Width</label>
                <div class="slider-container">
                    <input type="range" class="slider" min="0" max="20" value="2" 
                           oninput="changeStrokeWidth(this.value)">
                    <span class="slider-value" id="stroke-width-value">2</span>
                </div>
            </div>
        </div>
    `;
}

function addShape(type) {
    let shape;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    switch (type) {
        case 'rectangle':
            shape = new fabric.Rect({
                left: centerX - 75,
                top: centerY - 50,
                width: 150,
                height: 100,
                fill: '#6366f1',
                stroke: '#4f46e5',
                strokeWidth: 2
            });
            break;

        case 'circle':
            shape = new fabric.Circle({
                left: centerX - 60,
                top: centerY - 60,
                radius: 60,
                fill: '#ec4899',
                stroke: '#db2777',
                strokeWidth: 2
            });
            break;

        case 'triangle':
            shape = new fabric.Triangle({
                left: centerX - 60,
                top: centerY - 60,
                width: 120,
                height: 120,
                fill: '#10b981',
                stroke: '#059669',
                strokeWidth: 2
            });
            break;

        case 'line':
            shape = new fabric.Line([centerX - 100, centerY, centerX + 100, centerY], {
                stroke: '#333',
                strokeWidth: 3
            });
            break;

        case 'arrow':
            const arrow = new fabric.Group([
                new fabric.Line([0, 0, 100, 0], {
                    stroke: '#333',
                    strokeWidth: 3
                }),
                new fabric.Triangle({
                    left: 100,
                    top: 0,
                    width: 20,
                    height: 20,
                    fill: '#333',
                    angle: 90,
                    originX: 'center',
                    originY: 'center'
                })
            ], {
                left: centerX - 60,
                top: centerY
            });
            canvas.add(arrow);
            canvas.setActiveObject(arrow);
            canvas.renderAll();
            return;

        case 'star':
            shape = new fabric.Polygon([
                { x: 50, y: 0 },
                { x: 61, y: 35 },
                { x: 98, y: 35 },
                { x: 68, y: 57 },
                { x: 79, y: 91 },
                { x: 50, y: 70 },
                { x: 21, y: 91 },
                { x: 32, y: 57 },
                { x: 2, y: 35 },
                { x: 39, y: 35 }
            ], {
                left: centerX - 50,
                top: centerY - 45,
                fill: '#f59e0b',
                stroke: '#d97706',
                strokeWidth: 2
            });
            break;

        case 'heart':
            const heartPath = 'M 50,30 C 50,20 40,10 30,10 20,10 10,20 10,30 10,45 25,60 50,80 75,60 90,45 90,30 90,20 80,10 70,10 60,10 50,20 50,30 Z';
            shape = new fabric.Path(heartPath, {
                left: centerX - 50,
                top: centerY - 40,
                fill: '#ef4444',
                stroke: '#dc2626',
                strokeWidth: 2,
                scaleX: 1,
                scaleY: 1
            });
            break;

        case 'polygon':
            shape = new fabric.Polygon([
                { x: 50, y: 0 },
                { x: 100, y: 25 },
                { x: 100, y: 75 },
                { x: 50, y: 100 },
                { x: 0, y: 75 },
                { x: 0, y: 25 }
            ], {
                left: centerX - 50,
                top: centerY - 50,
                fill: '#8b5cf6',
                stroke: '#7c3aed',
                strokeWidth: 2
            });
            break;
    }

    if (shape) {
        canvas.add(shape);
        canvas.setActiveObject(shape);
        canvas.renderAll();
    }
}

function changeFillColor(color) {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.set('fill', color);
        canvas.renderAll();
    }
}

function changeStrokeColor(color) {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.set('stroke', color);
        canvas.renderAll();
    }
}

function changeStrokeWidth(width) {
    document.getElementById('stroke-width-value').textContent = width;
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.set('strokeWidth', parseInt(width));
        canvas.renderAll();
    }
}

// ==================== DRAWING TOOLS ====================

function getDrawPanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Drawing Tools</div>
            <button class="toolbar-btn" onclick="enableDrawing('pencil')" style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-pencil-alt"></i> Pencil
            </button>
            <button class="toolbar-btn" onclick="enableDrawing('brush')" style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-paint-brush"></i> Brush
            </button>
            <button class="toolbar-btn" onclick="enableEraser()" style="width: 100%;">
                <i class="fas fa-eraser"></i> Eraser
            </button>
        </div>

        <div class="panel-section">
            <div class="panel-title">Brush Color</div>
            <div class="color-grid">
                ${generateColorSwatches('brush')}
            </div>
            <div class="color-picker-wrapper" style="margin-top: 10px;">
                <div class="color-picker-btn">
                    <input type="color" id="brush-color-picker" value="#000000" onchange="changeBrushColor(this.value)">
                    <span style="padding: 10px;">Custom Color</span>
                </div>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Brush Size</div>
            <div class="slider-container">
                <input type="range" class="slider" min="1" max="50" value="5" 
                       oninput="changeBrushSize(this.value)" id="brush-size-slider">
                <span class="slider-value" id="brush-size-value">5</span>
            </div>
            <div class="brush-preview">
                <div class="brush-dot" id="brush-preview" style="width: 5px; height: 5px;"></div>
            </div>
        </div>

        <div class="panel-section">
            <button class="toolbar-btn" onclick="clearDrawing()" style="width: 100%;">
                <i class="fas fa-trash"></i> Clear All Drawing
            </button>
        </div>
    `;
}

function enableDrawing(type) {
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = document.getElementById('brush-color-picker')?.value || '#000000';
    canvas.freeDrawingBrush.width = parseInt(document.getElementById('brush-size-slider')?.value || 5);
}

function enableEraser() {
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = canvas.backgroundColor || '#ffffff';
    canvas.freeDrawingBrush.width = 20;
}

function changeBrushColor(color) {
    if (canvas.isDrawingMode) {
        canvas.freeDrawingBrush.color = color;
    }
}

function changeBrushSize(size) {
    document.getElementById('brush-size-value').textContent = size;
    const preview = document.getElementById('brush-preview');
    if (preview) {
        preview.style.width = size + 'px';
        preview.style.height = size + 'px';
    }
    if (canvas.isDrawingMode) {
        canvas.freeDrawingBrush.width = parseInt(size);
    }
}

function clearDrawing() {
    const objects = canvas.getObjects();
    objects.forEach(obj => {
        if (obj.type === 'path') {
            canvas.remove(obj);
        }
    });
    canvas.renderAll();
}

// ==================== IMAGE TOOLS ====================

function getImagePanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Upload Image</div>
            <input type="file" id="image-upload" accept="image/*" 
                   onchange="handleImageUpload(event)" 
                   style="display: none;">
            <button class="toolbar-btn" onclick="document.getElementById('image-upload').click()" 
                    style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-upload"></i> Upload from Computer
            </button>
        </div>

        <div class="panel-section">
            <div class="panel-title">Image Filters</div>
            <div class="button-group">
                <button class="icon-btn" onclick="applyFilter('grayscale')" title="Grayscale">
                    <i class="fas fa-adjust"></i>
                </button>
                <button class="icon-btn" onclick="applyFilter('sepia')" title="Sepia">
                    <i class="fas fa-sun"></i>
                </button>
                <button class="icon-btn" onclick="applyFilter('invert')" title="Invert">
                    <i class="fas fa-exchange-alt"></i>
                </button>
                <button class="icon-btn" onclick="applyFilter('blur')" title="Blur">
                    <i class="fas fa-circle"></i>
                </button>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Adjustments</div>
            <div style="margin-bottom: 15px;">
                <label class="property-label">Brightness</label>
                <div class="slider-container">
                    <input type="range" class="slider" min="-100" max="100" value="0" 
                           oninput="adjustBrightness(this.value)">
                    <span class="slider-value" id="brightness-value">0</span>
                </div>
            </div>
            <div>
                <label class="property-label">Opacity</label>
                <div class="slider-container">
                    <input type="range" class="slider" min="0" max="100" value="100" 
                           oninput="adjustOpacity(this.value)">
                    <span class="slider-value" id="opacity-value">100</span>
                </div>
            </div>
        </div>
    `;
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            fabric.Image.fromURL(e.target.result, function (img) {
                // Scale image to fit canvas
                const scale = Math.min(
                    canvas.width / 2 / img.width,
                    canvas.height / 2 / img.height
                );
                img.scale(scale);
                img.set({
                    left: canvas.width / 2,
                    top: canvas.height / 2,
                    originX: 'center',
                    originY: 'center'
                });
                canvas.add(img);
                canvas.setActiveObject(img);
                canvas.renderAll();
            });
        };
        reader.readAsDataURL(file);
    }
}

function applyFilter(filterType) {
    const activeObject = canvas.getActiveObject();
    if (activeObject && activeObject.type === 'image') {
        activeObject.filters = [];

        switch (filterType) {
            case 'grayscale':
                activeObject.filters.push(new fabric.Image.filters.Grayscale());
                break;
            case 'sepia':
                activeObject.filters.push(new fabric.Image.filters.Sepia());
                break;
            case 'invert':
                activeObject.filters.push(new fabric.Image.filters.Invert());
                break;
            case 'blur':
                activeObject.filters.push(new fabric.Image.filters.Blur({ blur: 0.5 }));
                break;
        }

        activeObject.applyFilters();
        canvas.renderAll();
    }
}

function adjustBrightness(value) {
    document.getElementById('brightness-value').textContent = value;
    const activeObject = canvas.getActiveObject();
    if (activeObject && activeObject.type === 'image') {
        activeObject.filters = activeObject.filters.filter(f => f.type !== 'Brightness');
        activeObject.filters.push(new fabric.Image.filters.Brightness({
            brightness: parseFloat(value) / 100
        }));
        activeObject.applyFilters();
        canvas.renderAll();
    }
}

function adjustOpacity(value) {
    document.getElementById('opacity-value').textContent = value;
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.set('opacity', parseFloat(value) / 100);
        canvas.renderAll();
    }
}

// ==================== BACKGROUND TOOLS ====================

function getBackgroundPanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Background Color</div>
            <div class="color-grid">
                ${generateColorSwatches('background')}
            </div>
            <div class="color-picker-wrapper" style="margin-top: 10px;">
                <div class="color-picker-btn">
                    <input type="color" id="bg-color-picker" value="#ffffff" onchange="changeBackgroundColor(this.value)">
                    <span style="padding: 10px;">Custom Color</span>
                </div>
            </div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Gradient Background</div>
            <button class="toolbar-btn" onclick="applyGradient('linear')" style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-grip-lines"></i> Linear Gradient
            </button>
            <button class="toolbar-btn" onclick="applyGradient('radial')" style="width: 100%;">
                <i class="fas fa-circle"></i> Radial Gradient
            </button>
        </div>

        <div class="panel-section">
            <div class="panel-title">Background Image</div>
            <input type="file" id="bg-image-upload" accept="image/*" 
                   onchange="handleBackgroundImageUpload(event)" 
                   style="display: none;">
            <button class="toolbar-btn" onclick="document.getElementById('bg-image-upload').click()" 
                    style="width: 100%; margin-bottom: 10px;">
                <i class="fas fa-image"></i> Upload Background
            </button>
            <button class="toolbar-btn" onclick="removeBackground()" style="width: 100%;">
                <i class="fas fa-times"></i> Remove Background
            </button>
        </div>
    `;
}

function changeBackgroundColor(color) {
    canvas.setBackgroundColor(color, canvas.renderAll.bind(canvas));
}

function applyGradient(type) {
    let gradient;
    if (type === 'linear') {
        gradient = new fabric.Gradient({
            type: 'linear',
            coords: { x1: 0, y1: 0, x2: canvas.width, y2: canvas.height },
            colorStops: [
                { offset: 0, color: '#6366f1' },
                { offset: 1, color: '#ec4899' }
            ]
        });
    } else {
        gradient = new fabric.Gradient({
            type: 'radial',
            coords: {
                x1: canvas.width / 2,
                y1: canvas.height / 2,
                r1: 0,
                x2: canvas.width / 2,
                y2: canvas.height / 2,
                r2: canvas.width / 2
            },
            colorStops: [
                { offset: 0, color: '#6366f1' },
                { offset: 1, color: '#ec4899' }
            ]
        });
    }
    canvas.setBackgroundColor(gradient, canvas.renderAll.bind(canvas));
}

function handleBackgroundImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            fabric.Image.fromURL(e.target.result, function (img) {
                canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
                    scaleX: canvas.width / img.width,
                    scaleY: canvas.height / img.height
                });
            });
        };
        reader.readAsDataURL(file);
    }
}

function removeBackground() {
    canvas.setBackgroundColor('#ffffff', canvas.renderAll.bind(canvas));
    canvas.setBackgroundImage(null, canvas.renderAll.bind(canvas));
}

// ==================== LAYERS PANEL ====================

function getLayersPanel() {
    return `
        <div class="panel-section">
            <div class="panel-title">Layers</div>
            <div id="layers-list"></div>
        </div>

        <div class="panel-section">
            <div class="panel-title">Layer Actions</div>
            <div class="button-group">
                <button class="icon-btn" onclick="bringToFront()" title="Bring to Front">
                    <i class="fas fa-arrow-up"></i>
                </button>
                <button class="icon-btn" onclick="sendToBack()" title="Send to Back">
                    <i class="fas fa-arrow-down"></i>
                </button>
                <button class="icon-btn" onclick="duplicateLayer()" title="Duplicate">
                    <i class="fas fa-copy"></i>
                </button>
                <button class="icon-btn" onclick="deleteSelected()" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
}

function updateLayersList() {
    const layersList = document.getElementById('layers-list');
    if (!layersList) return;

    const objects = canvas.getObjects();
    layersList.innerHTML = '';

    objects.reverse().forEach((obj, index) => {
        const actualIndex = objects.length - 1 - index;
        const layerItem = document.createElement('div');
        layerItem.className = 'layer-item';
        if (canvas.getActiveObject() === obj) {
            layerItem.classList.add('active');
        }

        let icon = 'fa-square';
        let typeName = 'Object';

        if (obj.type === 'i-text' || obj.type === 'text') {
            icon = 'fa-font';
            typeName = 'Text';
        } else if (obj.type === 'image') {
            icon = 'fa-image';
            typeName = 'Image';
        } else if (obj.type === 'path') {
            icon = 'fa-pen';
            typeName = 'Drawing';
        } else if (obj.type === 'circle') {
            icon = 'fa-circle';
            typeName = 'Circle';
        } else if (obj.type === 'rect') {
            icon = 'fa-square';
            typeName = 'Rectangle';
        }

        layerItem.innerHTML = `
            <div class="layer-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="layer-info">
                <div class="layer-name">Layer ${actualIndex + 1}</div>
                <div class="layer-type">${typeName}</div>
            </div>
        `;

        layerItem.onclick = () => {
            canvas.setActiveObject(obj);
            canvas.renderAll();
            updateLayersList();
        };

        layersList.appendChild(layerItem);
    });
}

function bringToFront() {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        canvas.bringToFront(activeObject);
        canvas.renderAll();
        updateLayersList();
    }
}

function sendToBack() {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        canvas.sendToBack(activeObject);
        canvas.renderAll();
        updateLayersList();
    }
}

function duplicateLayer() {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.clone(function (cloned) {
            cloned.set({
                left: cloned.left + 20,
                top: cloned.top + 20
            });
            canvas.add(cloned);
            canvas.setActiveObject(cloned);
            canvas.renderAll();
        });
    }
}

// ==================== PROPERTIES PANEL ====================

function handleSelection(e) {
    selectedObject = e.selected[0];
    updatePropertiesPanel();
    updateSelectedInfo();
    if (currentTool === 'layers') {
        updateLayersList();
    }
}

function clearSelection() {
    selectedObject = null;
    updatePropertiesPanel();
    updateSelectedInfo();
}

function updatePropertiesPanel() {
    const panel = document.getElementById('properties-panel');

    if (!selectedObject) {
        panel.innerHTML = `
            <div class="panel-section">
                <div class="panel-title">Properties</div>
                <p style="color: #999; font-size: 13px;">
                    Select an object to view its properties
                </p>
            </div>
        `;
        return;
    }

    let html = `<div class="panel-section"><div class="panel-title">Properties</div></div>`;

    // Position
    html += `
        <div class="property-group">
            <div class="property-label">Position</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <label style="font-size: 11px; color: #999;">X</label>
                    <input type="number" class="property-input" value="${Math.round(selectedObject.left)}" 
                           onchange="updateProperty('left', this.value)">
                </div>
                <div>
                    <label style="font-size: 11px; color: #999;">Y</label>
                    <input type="number" class="property-input" value="${Math.round(selectedObject.top)}" 
                           onchange="updateProperty('top', this.value)">
                </div>
            </div>
        </div>
    `;

    // Size
    html += `
        <div class="property-group">
            <div class="property-label">Size</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                    <label style="font-size: 11px; color: #999;">Width</label>
                    <input type="number" class="property-input" value="${Math.round(selectedObject.width * selectedObject.scaleX)}" 
                           onchange="updateSize('width', this.value)">
                </div>
                <div>
                    <label style="font-size: 11px; color: #999;">Height</label>
                    <input type="number" class="property-input" value="${Math.round(selectedObject.height * selectedObject.scaleY)}" 
                           onchange="updateSize('height', this.value)">
                </div>
            </div>
        </div>
    `;

    // Rotation
    html += `
        <div class="property-group">
            <div class="property-label">Rotation</div>
            <div class="slider-container">
                <input type="range" class="slider" min="0" max="360" value="${selectedObject.angle || 0}" 
                       oninput="updateProperty('angle', this.value)">
                <span class="slider-value">${Math.round(selectedObject.angle || 0)}°</span>
            </div>
        </div>
    `;

    // Text-specific properties
    if (selectedObject.type === 'i-text' || selectedObject.type === 'text') {
        html += `
            <div class="property-group">
                <div class="property-label">Font Size</div>
                <div class="slider-container">
                    <input type="range" class="slider" min="8" max="120" value="${selectedObject.fontSize}" 
                           oninput="updateProperty('fontSize', this.value)">
                    <span class="slider-value">${selectedObject.fontSize}</span>
                </div>
            </div>
            
            <div class="property-group">
                <div class="property-label">Text Align</div>
                <div class="button-group">
                    <button class="icon-btn ${selectedObject.textAlign === 'left' ? 'active' : ''}" 
                            onclick="updateProperty('textAlign', 'left')">
                        <i class="fas fa-align-left"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.textAlign === 'center' ? 'active' : ''}" 
                            onclick="updateProperty('textAlign', 'center')">
                        <i class="fas fa-align-center"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.textAlign === 'right' ? 'active' : ''}" 
                            onclick="updateProperty('textAlign', 'right')">
                        <i class="fas fa-align-right"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.textAlign === 'justify' ? 'active' : ''}" 
                            onclick="updateProperty('textAlign', 'justify')">
                        <i class="fas fa-align-justify"></i>
                    </button>
                </div>
            </div>
            
            <div class="property-group">
                <div class="property-label">Text Style</div>
                <div class="button-group">
                    <button class="icon-btn ${selectedObject.fontWeight === 'bold' ? 'active' : ''}" 
                            onclick="toggleBold()">
                        <i class="fas fa-bold"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.fontStyle === 'italic' ? 'active' : ''}" 
                            onclick="toggleItalic()">
                        <i class="fas fa-italic"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.underline ? 'active' : ''}" 
                            onclick="toggleUnderline()">
                        <i class="fas fa-underline"></i>
                    </button>
                    <button class="icon-btn ${selectedObject.linethrough ? 'active' : ''}" 
                            onclick="toggleStrikethrough()">
                        <i class="fas fa-strikethrough"></i>
                    </button>
                </div>
            </div>
        `;
    }

    panel.innerHTML = html;
}

function updateProperty(property, value) {
    if (selectedObject) {
        selectedObject.set(property, parseFloat(value) || value);
        canvas.renderAll();
        updatePropertiesPanel();
    }
}

function updateSize(dimension, value) {
    if (selectedObject) {
        const numValue = parseFloat(value);
        if (dimension === 'width') {
            selectedObject.scaleX = numValue / selectedObject.width;
        } else {
            selectedObject.scaleY = numValue / selectedObject.height;
        }
        canvas.renderAll();
    }
}

function toggleBold() {
    if (selectedObject && (selectedObject.type === 'i-text' || selectedObject.type === 'text')) {
        selectedObject.set('fontWeight', selectedObject.fontWeight === 'bold' ? 'normal' : 'bold');
        canvas.renderAll();
        updatePropertiesPanel();
    }
}

function toggleItalic() {
    if (selectedObject && (selectedObject.type === 'i-text' || selectedObject.type === 'text')) {
        selectedObject.set('fontStyle', selectedObject.fontStyle === 'italic' ? 'normal' : 'italic');
        canvas.renderAll();
        updatePropertiesPanel();
    }
}

function toggleUnderline() {
    if (selectedObject && (selectedObject.type === 'i-text' || selectedObject.type === 'text')) {
        selectedObject.set('underline', !selectedObject.underline);
        canvas.renderAll();
        updatePropertiesPanel();
    }
}

function toggleStrikethrough() {
    if (selectedObject && (selectedObject.type === 'i-text' || selectedObject.type === 'text')) {
        selectedObject.set('linethrough', !selectedObject.linethrough);
        canvas.renderAll();
        updatePropertiesPanel();
    }
}

// ==================== UTILITY FUNCTIONS ====================

function generateColorSwatches(type) {
    const colors = [
        '#000000', '#FFFFFF', '#6366f1', '#ec4899', '#10b981',
        '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16',
        '#f97316', '#14b8a6', '#a855f7', '#eab308', '#64748b'
    ];

    return colors.map(color =>
        `<div class="color-swatch" style="background: ${color};" 
              onclick="applyColor('${type}', '${color}')"></div>`
    ).join('');
}

function applyColor(type, color) {
    switch (type) {
        case 'text':
            changeTextColor(color);
            break;
        case 'fill':
            changeFillColor(color);
            break;
        case 'stroke':
            changeStrokeColor(color);
            break;
        case 'brush':
            changeBrushColor(color);
            if (document.getElementById('brush-color-picker')) {
                document.getElementById('brush-color-picker').value = color;
            }
            break;
        case 'background':
            changeBackgroundColor(color);
            break;
    }
}

function updateSelectedInfo() {
    const info = document.getElementById('selected-info');
    if (selectedObject) {
        let type = selectedObject.type;
        if (type === 'i-text') type = 'Text';
        info.textContent = `Selected: ${type.charAt(0).toUpperCase() + type.slice(1)}`;
    } else {
        info.textContent = 'No object selected';
    }
}

// ==================== HISTORY & UNDO/REDO ====================

function saveState() {
    const json = JSON.stringify(canvas.toJSON());
    history = history.slice(0, historyStep + 1);
    history.push(json);
    historyStep++;

    // Limit history to 50 steps
    if (history.length > 50) {
        history.shift();
        historyStep--;
    }
}

function undoAction() {
    if (historyStep > 0) {
        historyStep--;
        canvas.loadFromJSON(history[historyStep], function () {
            canvas.renderAll();
        });
    }
}

function redoAction() {
    if (historyStep < history.length - 1) {
        historyStep++;
        canvas.loadFromJSON(history[historyStep], function () {
            canvas.renderAll();
        });
    }
}

// ==================== CANVAS ACTIONS ====================

function clearCanvas() {
    if (confirm('Are you sure you want to clear the entire canvas?')) {
        canvas.clear();
        canvas.setBackgroundColor('#ffffff', canvas.renderAll.bind(canvas));
        saveState();
    }
}

function deleteSelected() {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        canvas.remove(activeObject);
        canvas.renderAll();
    }
}

let clipboard;

function copySelected() {
    const activeObject = canvas.getActiveObject();
    if (activeObject) {
        activeObject.clone(function (cloned) {
            clipboard = cloned;
        });
    }
}

function pasteSelected() {
    if (clipboard) {
        clipboard.clone(function (cloned) {
            canvas.discardActiveObject();
            cloned.set({
                left: cloned.left + 20,
                top: cloned.top + 20,
                evented: true,
            });
            if (cloned.type === 'activeSelection') {
                cloned.canvas = canvas;
                cloned.forEachObject(function (obj) {
                    canvas.add(obj);
                });
                cloned.setCoords();
            } else {
                canvas.add(cloned);
            }
            clipboard.top += 20;
            clipboard.left += 20;
            canvas.setActiveObject(cloned);
            canvas.requestRenderAll();
        });
    }
}

// ==================== ZOOM CONTROLS ====================

let zoomLevel = 1;

function zoomIn() {
    zoomLevel = Math.min(zoomLevel + 0.1, 3);
    canvas.setZoom(zoomLevel);
    updateZoomDisplay();
}

function zoomOut() {
    zoomLevel = Math.max(zoomLevel - 0.1, 0.1);
    canvas.setZoom(zoomLevel);
    updateZoomDisplay();
}

function updateZoomDisplay() {
    document.getElementById('zoom-level').textContent = Math.round(zoomLevel * 100) + '%';
}

// ==================== SAVE & EXPORT ====================

function saveDesign() {
    const title = document.getElementById('design-title').value || 'Untitled Design';
    const json = JSON.stringify(canvas.toJSON());

    // Create thumbnail
    const dataURL = canvas.toDataURL({
        format: 'png',
        quality: 0.8,
        multiplier: 0.2
    });

    // Send to server
    fetch('/api/save-design', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            canvas_data: json,
            thumbnail: dataURL
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Design saved successfully!');
            } else {
                alert('Error saving design: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error saving design');
        });
}

function downloadDesign(format) {
    const title = document.getElementById('design-title').value || 'design';

    if (format === 'png') {
        const dataURL = canvas.toDataURL({
            format: 'png',
            quality: 1
        });
        const link = document.createElement('a');
        link.download = title + '.png';
        link.href = dataURL;
        link.click();
    } else if (format === 'pdf') {
        // PDF export would require jsPDF
        alert('PDF export coming soon!');
    } else if (format === 'json') {
        const json = JSON.stringify(canvas.toJSON());
        const blob = new Blob([json], { type: 'application/json' });
        const link = document.createElement('a');
        link.download = title + '.json';
        link.href = URL.createObjectURL(blob);
        link.click();
    }
}
