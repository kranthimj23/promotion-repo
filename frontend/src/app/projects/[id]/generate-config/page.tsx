'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';

export default function GenerateConfigPage() {
    const params = useParams();
    const projectId = params.id as string;
    const [project, setProject] = useState<any>(null);
    const [formData, setFormData] = useState({
        environment: '',
        releaseBranch: '',
    });
    const [loading, setLoading] = useState(false);
    const [fetchingProject, setFetchingProject] = useState(true);
    const [result, setResult] = useState<any>(null);

    useEffect(() => {
        async function fetchProject() {
            try {
                const res = await fetch(`http://localhost:3001/api/projects/${projectId}`);
                if (res.ok) {
                    const data = await res.json();
                    setProject(data);
                    // Pre-fill environment if available
                    if (data.environments && data.environments.length > 0) {
                        setFormData(prev => ({ ...prev, environment: data.environments[0].name }));
                    }
                }
            } catch (err) {
                console.error('Failed to fetch project context:', err);
            } finally {
                setFetchingProject(false);
            }
        }
        fetchProject();
    }, [projectId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await fetch('http://localhost:3001/api/cd/generate-config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...formData, projectId }),
            });
            const data = await res.json();
            setResult(data);
        } catch (error: any) {
            setResult({ success: false, error: error.message });
        } finally {
            setLoading(false);
        }
    };

    if (fetchingProject) return <div>Loading project context...</div>;

    return (
        <div style={{ maxWidth: '800px' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1 style={{ fontSize: '1.875rem', fontWeight: 700, marginBottom: '0.5rem' }}>Generate Config</h1>
                <p style={{ color: 'var(--muted-foreground)' }}>Project: <strong>{project?.displayName || projectId}</strong></p>
            </div>

            <div className="card">
                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1.5rem' }}>
                    <div style={{ display: 'grid', gap: '0.5rem' }}>
                        <label style={{ fontSize: '0.875rem', fontWeight: 500 }}>Environment</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g. prod"
                            value={formData.environment}
                            onChange={(e) => setFormData({ ...formData, environment: e.target.value })}
                            style={{ padding: '0.5rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)', background: 'var(--background)' }}
                        />
                    </div>
                    <div style={{ display: 'grid', gap: '0.5rem' }}>
                        <label style={{ fontSize: '0.875rem', fontWeight: 500 }}>Release Branch</label>
                        <input
                            type="text"
                            className="input"
                            placeholder="e.g. release/v1.0"
                            value={formData.releaseBranch}
                            onChange={(e) => setFormData({ ...formData, releaseBranch: e.target.value })}
                            style={{ padding: '0.5rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)', background: 'var(--background)' }}
                        />
                    </div>

                    <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: 'fit-content' }}>
                        {loading ? 'Generating...' : 'Generate Config'}
                    </button>
                </form>
            </div>

            {result && (
                <div style={{ marginTop: '2rem' }}>
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem' }}>Result</h2>
                    <pre style={{
                        background: 'var(--muted)',
                        padding: '1rem',
                        borderRadius: 'var(--radius)',
                        overflowX: 'auto',
                        fontSize: '0.875rem',
                        border: result.success ? '1px solid var(--success)' : '1px solid var(--destructive)'
                    }}>
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}
