/**
 * Q360 DataTables Integration
 * Dinamik cədvəllər üçün server-side DataTables inteqrasiyası
 */

class Q360DataTable {
    /**
     * DataTable yaradır və konfiqurasiya edir
     *
     * @param {string} selector - Cədvəl element seçicisi (CSS selector)
     * @param {string} apiUrl - API endpoint URL-i
     * @param {Array} columns - Sütun konfiqurasiyası
     * @param {Object} options - Əlavə parametrlər
     */
    constructor(selector, apiUrl, columns, options = {}) {
        this.selector = selector;
        this.apiUrl = apiUrl;
        this.columns = columns;
        this.options = options;
        this.table = null;
        this.init();
    }

    /**
     * DataTable-i başladır
     */
    init() {
        const defaultOptions = {
            processing: true,
            serverSide: true,
            ajax: {
                url: this.apiUrl,
                type: 'GET',
                headers: this.getCSRFHeaders(),
                dataSrc: 'data',
                error: (xhr, error, code) => {
                    console.error('DataTables AJAX error:', error, code);
                    this.handleError(xhr, error);
                }
            },
            columns: this.columns,
            pageLength: 25,
            lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Hamısı"]],
            language: {
                processing: "Yüklənir...",
                search: "Axtarış:",
                lengthMenu: "Göstər _MENU_ qeyd",
                info: "_START_-dən _END_-ə qədər (_TOTAL_ qeyd)",
                infoEmpty: "0-dan 0-a qədər (0 qeyd)",
                infoFiltered: "(_MAX_ qeyd arasından)",
                loadingRecords: "Yüklənir...",
                zeroRecords: "Uyğun qeyd tapılmadı",
                emptyTable: "Cədvəldə məlumat yoxdur",
                paginate: {
                    first: "İlk",
                    previous: "Əvvəlki",
                    next: "Növbəti",
                    last: "Son"
                },
                aria: {
                    sortAscending: ": artan sıralamaq üçün aktivləşdirin",
                    sortDescending: ": azalan sıralamaq üçün aktivləşdirin"
                }
            },
            dom: '<"flex justify-between items-center mb-4"lf>rt<"flex justify-between items-center mt-4"ip>',
            order: [[0, 'desc']],
            ...this.options
        };

        // DataTable yaradır
        this.table = $(this.selector).DataTable(defaultOptions);

        // Əlavə event listener-lər
        this.attachEventListeners();
    }

    /**
     * CSRF token headers qaytarır
     */
    getCSRFHeaders() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                          document.querySelector('meta[name="csrf-token"]')?.content;

        return csrfToken ? { 'X-CSRFToken': csrfToken } : {};
    }

    /**
     * Xəta handler
     */
    handleError(xhr, error) {
        let errorMessage = 'Məlumat yüklənərkən xəta baş verdi.';

        if (xhr.status === 403) {
            errorMessage = 'Bu əməliyyat üçün icazəniz yoxdur.';
        } else if (xhr.status === 404) {
            errorMessage = 'API endpoint tapılmadı.';
        } else if (xhr.status === 500) {
            errorMessage = 'Server xətası baş verdi.';
        }

        // Toast bildiriş göstər
        if (typeof showNotification === 'function') {
            showNotification(errorMessage, 'error');
        } else {
            alert(errorMessage);
        }
    }

    /**
     * Event listener-lər əlavə edir
     */
    attachEventListeners() {
        // Sətir klikləri
        if (this.options.onRowClick) {
            $(this.selector).on('click', 'tbody tr', (e) => {
                const data = this.table.row(e.currentTarget).data();
                this.options.onRowClick(data, e);
            });
        }

        // Custom filter düymələri
        if (this.options.customFilters) {
            Object.keys(this.options.customFilters).forEach(filterId => {
                $(`#${filterId}`).on('change', () => {
                    this.applyCustomFilter(filterId);
                });
            });
        }
    }

    /**
     * Custom filter tətbiq edir
     */
    applyCustomFilter(filterId) {
        const filterValue = $(`#${filterId}`).val();
        const columnIndex = this.options.customFilters[filterId];

        this.table.column(columnIndex).search(filterValue).draw();
    }

    /**
     * Cədvəli yenidən yükləyir
     */
    reload() {
        this.table.ajax.reload(null, false); // false = səhifə resetlənməsin
    }

    /**
     * Seçilmiş sətirləri qaytarır
     */
    getSelectedRows() {
        return this.table.rows('.selected').data().toArray();
    }

    /**
     * Bütün məlumatları export edir
     */
    exportData(format = 'csv') {
        // Export funksionallığı
        console.log(`Export format: ${format}`);
        // TODO: Backend export endpoint çağırış
    }

    /**
     * Cədvəli məhv edir
     */
    destroy() {
        if (this.table) {
            this.table.destroy();
            this.table = null;
        }
    }
}

/**
 * İstifadəçi cədvəli üçün xüsusi konfiqurasiya
 */
function initializeUserTable(selector = '#user-table') {
    const columns = [
        {
            data: 'id',
            title: 'ID',
            width: '50px'
        },
        {
            data: 'username',
            title: 'İstifadəçi adı',
            render: (data, type, row) => {
                return `<a href="/accounts/profile/${row.id}/" class="text-blue-600 hover:underline">${data}</a>`;
            }
        },
        {
            data: 'full_name',
            title: 'Ad Soyad'
        },
        {
            data: 'email',
            title: 'E-poçt'
        },
        {
            data: 'department_name',
            title: 'Şöbə',
            defaultContent: '-'
        },
        {
            data: 'position',
            title: 'Vəzifə',
            defaultContent: '-'
        },
        {
            data: 'role_display',
            title: 'Rol',
            render: (data, type, row) => {
                const roleColors = {
                    'Superadmin': 'bg-red-100 text-red-800',
                    'Admin': 'bg-orange-100 text-orange-800',
                    'Manager': 'bg-blue-100 text-blue-800',
                    'Employee': 'bg-green-100 text-green-800'
                };
                const colorClass = roleColors[data] || 'bg-gray-100 text-gray-800';
                return `<span class="px-2 py-1 rounded text-xs ${colorClass}">${data}</span>`;
            }
        },
        {
            data: 'is_active',
            title: 'Status',
            render: (data, type, row) => {
                if (data) {
                    return '<span class="px-2 py-1 rounded text-xs bg-green-100 text-green-800">Aktiv</span>';
                } else {
                    return '<span class="px-2 py-1 rounded text-xs bg-gray-100 text-gray-800">Deaktiv</span>';
                }
            }
        },
        {
            data: null,
            title: 'Əməliyyatlar',
            orderable: false,
            render: (data, type, row) => {
                return `
                    <div class="flex gap-2">
                        <a href="/accounts/profile/${row.id}/" class="text-blue-600 hover:text-blue-800" title="Bax">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                            </svg>
                        </a>
                        <a href="/accounts/${row.id}/edit/" class="text-yellow-600 hover:text-yellow-800" title="Redaktə">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                            </svg>
                        </a>
                    </div>
                `;
            }
        }
    ];

    const options = {
        order: [[0, 'desc']],
        pageLength: 25,
        customFilters: {
            'role-filter': 6, // Rol sütunu
            'status-filter': 7 // Status sütunu
        }
    };

    return new Q360DataTable(
        selector,
        '/api/accounts/users/datatable/',
        columns,
        options
    );
}

/**
 * Audit log cədvəli
 */
function initializeAuditLogTable(selector = '#audit-log-table') {
    const columns = [
        { data: 'id', title: 'ID', width: '50px' },
        { data: 'user__username', title: 'İstifadəçi' },
        { data: 'action', title: 'Əməliyyat' },
        { data: 'model_name', title: 'Model' },
        {
            data: 'severity',
            title: 'Şiddət',
            render: (data) => {
                const colors = {
                    'info': 'bg-blue-100 text-blue-800',
                    'warning': 'bg-yellow-100 text-yellow-800',
                    'critical': 'bg-red-100 text-red-800'
                };
                return `<span class="px-2 py-1 rounded text-xs ${colors[data]}">${data}</span>`;
            }
        },
        {
            data: 'threat_level',
            title: 'Təhlükə',
            render: (data) => {
                const colors = {
                    'none': 'bg-gray-100 text-gray-800',
                    'low': 'bg-blue-100 text-blue-800',
                    'medium': 'bg-yellow-100 text-yellow-800',
                    'high': 'bg-orange-100 text-orange-800',
                    'critical': 'bg-red-100 text-red-800'
                };
                return `<span class="px-2 py-1 rounded text-xs ${colors[data]}">${data}</span>`;
            }
        },
        { data: 'created_at', title: 'Tarix' }
    ];

    return new Q360DataTable(
        selector,
        '/api/audit/logs/datatable/',
        columns,
        { order: [[0, 'desc']] }
    );
}

// Global scope-a əlavə et
window.Q360DataTable = Q360DataTable;
window.initializeUserTable = initializeUserTable;
window.initializeAuditLogTable = initializeAuditLogTable;
