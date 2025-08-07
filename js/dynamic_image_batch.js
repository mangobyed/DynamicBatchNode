/**
 * Dynamic Image Batch - Proper Dynamic Input Management
 * Adds/removes actual inputs based on input_count value
 */

import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "DynamicImageBatch",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "DynamicImageBatch") {
            return;
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onNodeCreated?.apply(this, arguments);
            
            const node = this;
            
            // Function to update inputs based on input_count
            function updateInputs() {
                const inputCountWidget = node.widgets?.find(w => w.name === "input_count");
                if (!inputCountWidget) {
                    console.log("DynamicImageBatch: input_count widget not found");
                    return;
                }
                
                const targetCount = inputCountWidget.value || 2;
                console.log(`DynamicImageBatch: Updating to ${targetCount} inputs`);
                
                // Count current image inputs
                let currentImageInputs = 0;
                const imageInputs = [];
                for (let i = 0; i < node.inputs.length; i++) {
                    if (node.inputs[i].name.startsWith("image_")) {
                        imageInputs.push(i);
                        currentImageInputs++;
                    }
                }
                
                console.log(`DynamicImageBatch: Current inputs: ${currentImageInputs}, target: ${targetCount}`);
                
                // Remove excess inputs (from the end)
                while (currentImageInputs > targetCount) {
                    const lastImageInputIndex = imageInputs.pop();
                    if (lastImageInputIndex !== undefined) {
                        console.log(`DynamicImageBatch: Removing input at index ${lastImageInputIndex}`);
                        node.removeInput(lastImageInputIndex);
                        currentImageInputs--;
                    }
                }
                
                // Add missing inputs
                while (currentImageInputs < targetCount) {
                    currentImageInputs++;
                    const inputName = `image_${currentImageInputs}`;
                    console.log(`DynamicImageBatch: Adding input ${inputName}`);
                    node.addInput(inputName, "IMAGE");
                }
                
                // Update node size and redraw
                node.setSize(node.computeSize());
                if (node.graph) {
                    node.graph.setDirtyCanvas(true, true);
                }
            }
            
            // Set up widget callback
            const setupCallback = () => {
                const inputCountWidget = node.widgets?.find(w => w.name === "input_count");
                if (inputCountWidget) {
                    console.log("DynamicImageBatch: Setting up input_count callback");
                    
                    // Store original callback
                    const originalCallback = inputCountWidget.callback;
                    
                    // Replace with our callback
                    inputCountWidget.callback = function(value) {
                        console.log(`DynamicImageBatch: input_count changed to ${value}`);
                        if (originalCallback) {
                            originalCallback.apply(this, arguments);
                        }
                        updateInputs();
                    };
                    
                    // Initial update
                    updateInputs();
                } else {
                    console.log("DynamicImageBatch: Widget not ready, retrying...");
                    setTimeout(setupCallback, 100);
                }
            };
            
            // Start setup after a brief delay
            setTimeout(setupCallback, 100);
            
            return r;
        };

        return nodeType;
    }
});