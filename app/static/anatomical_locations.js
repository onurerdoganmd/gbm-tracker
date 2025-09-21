/**
 * Anatomical Locations Data Structure for GBM Tracker
 * Comprehensive brain anatomy locations organized by categories
 */

const ANATOMICAL_LOCATIONS = {
    "Supratentorial": [
        "Frontal lobe",
        "Temporal lobe",
        "Parietal lobe",
        "Occipital lobe"
    ],
    "Deep Gray Matter": [
        "Thalamus",
        "Caudate nucleus",
        "Putamen",
        "Globus pallidus"
    ],
    "Commissural/Periventricular": [
        "Corpus callosum",
        "Fornix",
        "Septum pellucidum",
        "Periventricular white matter"
    ],
    "Diencephalon/Midline": [
        "Hypothalamus",
        "Pineal region"
    ],
    "Brainstem": [
        "Midbrain",
        "Pons",
        "Medulla oblongata"
    ],
    "Infratentorial": [
        "Cerebellar hemispheres",
        "Cerebellar vermis",
        "Cerebellopontine angle",
        "Fourth ventricle region"
    ],
    "Ventricular System": [
        "Lateral ventricle",
        "Third ventricle",
        "Fourth ventricle"
    ],
    "Spinal Cord": [
        "Cervical spinal cord",
        "Thoracic spinal cord",
        "Lumbar spinal cord"
    ]
};

/**
 * AnatomicalLocationSelector - A reusable component for anatomical location selection
 */
class AnatomicalLocationSelector {
    constructor(inputElementId, modalElementId = null) {
        this.inputElement = document.getElementById(inputElementId);
        this.modalElementId = modalElementId || `${inputElementId}_anatomical_modal`;
        this.selectedLocation = '';
        this.selectedCategory = '';

        this.init();
    }

    init() {
        this.createModal();
        this.setupEventListeners();
    }

    createModal() {
        // Create modal HTML
        const modalHTML = `
            <div id="${this.modalElementId}" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full hidden z-50">
                <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-md bg-white">
                    <div class="mt-3">
                        <!-- Modal Header -->
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-lg font-medium text-gray-900">Select Anatomical Location</h3>
                            <button id="${this.modalElementId}_close" class="text-gray-400 hover:text-gray-600">
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                            </button>
                        </div>

                        <!-- Search Box -->
                        <div class="mb-4">
                            <input type="text" id="${this.modalElementId}_search"
                                   placeholder="Search anatomical locations..."
                                   class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                        </div>

                        <!-- Categories and Locations -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
                            ${this.generateCategoriesHTML()}
                        </div>

                        <!-- Selected Location Display -->
                        <div id="${this.modalElementId}_selected" class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded hidden">
                            <div class="flex justify-between items-center">
                                <div>
                                    <div class="text-sm font-medium text-blue-900">Selected:</div>
                                    <div id="${this.modalElementId}_selected_text" class="text-blue-800"></div>
                                </div>
                                <button id="${this.modalElementId}_confirm" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm">
                                    Confirm Selection
                                </button>
                            </div>
                        </div>

                        <!-- Manual Entry Option -->
                        <div class="mt-4 border-t pt-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">Or enter custom location:</label>
                            <div class="flex space-x-2">
                                <input type="text" id="${this.modalElementId}_custom"
                                       placeholder="Enter custom anatomical location..."
                                       class="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                                <button id="${this.modalElementId}_use_custom" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm">
                                    Use Custom
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Insert modal into DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById(this.modalElementId);
    }

    generateCategoriesHTML() {
        let html = '';

        Object.entries(ANATOMICAL_LOCATIONS).forEach(([category, locations]) => {
            html += `
                <div class="category-section">
                    <h4 class="font-medium text-gray-900 mb-2 text-sm">${category}</h4>
                    <div class="space-y-1">
                        ${locations.map(location => `
                            <button class="location-btn w-full text-left px-3 py-2 text-sm rounded hover:bg-blue-50 hover:text-blue-700 transition-colors"
                                    data-category="${category}" data-location="${location}">
                                ${location}
                            </button>
                        `).join('')}
                    </div>
                </div>
            `;
        });

        return html;
    }

    setupEventListeners() {
        // Add button to open modal next to input
        this.addLocationButton();

        // Modal close events
        document.getElementById(`${this.modalElementId}_close`).addEventListener('click', () => this.closeModal());

        // Search functionality
        document.getElementById(`${this.modalElementId}_search`).addEventListener('input', (e) => this.handleSearch(e.target.value));

        // Location selection
        this.modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('location-btn')) {
                this.selectLocation(e.target.dataset.category, e.target.dataset.location);
            }
        });

        // Confirm selection
        document.getElementById(`${this.modalElementId}_confirm`).addEventListener('click', () => this.confirmSelection());

        // Custom location
        document.getElementById(`${this.modalElementId}_use_custom`).addEventListener('click', () => this.useCustomLocation());

        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                this.closeModal();
            }
        });
    }

    addLocationButton() {
        // Wrap the input in a container if not already wrapped
        if (!this.inputElement.parentElement.classList.contains('location-input-container')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'location-input-container relative';
            this.inputElement.parentNode.insertBefore(wrapper, this.inputElement);
            wrapper.appendChild(this.inputElement);
        }

        // Add button
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs transition-colors';
        button.textContent = 'Browse';
        button.addEventListener('click', () => this.openModal());

        this.inputElement.parentElement.appendChild(button);

        // Update input padding to accommodate button
        this.inputElement.classList.add('pr-20');
    }

    openModal() {
        this.modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Focus search box
        document.getElementById(`${this.modalElementId}_search`).focus();

        // Reset modal state
        this.resetModalState();
    }

    closeModal() {
        this.modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }

    resetModalState() {
        // Clear search
        document.getElementById(`${this.modalElementId}_search`).value = '';

        // Clear custom input
        document.getElementById(`${this.modalElementId}_custom`).value = '';

        // Hide selected display
        document.getElementById(`${this.modalElementId}_selected`).classList.add('hidden');

        // Show all locations
        this.showAllLocations();

        // Clear selection state
        this.selectedLocation = '';
        this.selectedCategory = '';
    }

    handleSearch(searchTerm) {
        const term = searchTerm.toLowerCase();
        const locationBtns = this.modal.querySelectorAll('.location-btn');
        const categories = this.modal.querySelectorAll('.category-section');

        if (term === '') {
            this.showAllLocations();
            return;
        }

        // Hide all categories first
        categories.forEach(cat => cat.style.display = 'none');

        // Show matching locations and their categories
        const visibleCategories = new Set();
        locationBtns.forEach(btn => {
            const location = btn.dataset.location.toLowerCase();
            const category = btn.dataset.category.toLowerCase();

            if (location.includes(term) || category.includes(term)) {
                btn.style.display = 'block';
                visibleCategories.add(btn.dataset.category);
            } else {
                btn.style.display = 'none';
            }
        });

        // Show categories that have visible locations
        categories.forEach(cat => {
            const categoryName = cat.querySelector('h4').textContent;
            if (visibleCategories.has(categoryName)) {
                cat.style.display = 'block';
            }
        });
    }

    showAllLocations() {
        const locationBtns = this.modal.querySelectorAll('.location-btn');
        const categories = this.modal.querySelectorAll('.category-section');

        locationBtns.forEach(btn => btn.style.display = 'block');
        categories.forEach(cat => cat.style.display = 'block');
    }

    selectLocation(category, location) {
        this.selectedCategory = category;
        this.selectedLocation = location;

        // Update selected display
        const selectedDiv = document.getElementById(`${this.modalElementId}_selected`);
        const selectedText = document.getElementById(`${this.modalElementId}_selected_text`);

        selectedText.textContent = `${location} (${category})`;
        selectedDiv.classList.remove('hidden');

        // Highlight selected button
        this.modal.querySelectorAll('.location-btn').forEach(btn => {
            btn.classList.remove('bg-blue-100', 'text-blue-800', 'border-blue-300');
        });

        const selectedBtn = this.modal.querySelector(`[data-location="${location}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('bg-blue-100', 'text-blue-800', 'border-blue-300');
        }
    }

    confirmSelection() {
        if (this.selectedLocation) {
            this.inputElement.value = this.selectedLocation;

            // Trigger change event
            const event = new Event('change', { bubbles: true });
            this.inputElement.dispatchEvent(event);

            this.closeModal();
        }
    }

    useCustomLocation() {
        const customInput = document.getElementById(`${this.modalElementId}_custom`);
        const customValue = customInput.value.trim();

        if (customValue) {
            this.inputElement.value = customValue;

            // Trigger change event
            const event = new Event('change', { bubbles: true });
            this.inputElement.dispatchEvent(event);

            this.closeModal();
        }
    }

    // Static method to initialize all selectors on a page
    static initializeAll() {
        // Look for input fields with data-anatomical-selector attribute
        document.querySelectorAll('input[data-anatomical-selector]').forEach(input => {
            new AnatomicalLocationSelector(input.id);
        });
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ANATOMICAL_LOCATIONS, AnatomicalLocationSelector };
}

// Auto-initialize when DOM is loaded
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        AnatomicalLocationSelector.initializeAll();
    });
}