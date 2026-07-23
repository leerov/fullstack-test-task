"use client";

import { useState } from "react";
import { Alert, Badge, Card, Col, Container, Row } from "react-bootstrap";
import { useFiles } from "../hooks/useFiles";
import { useAlerts } from "../hooks/useAlerts";
import { useFileUpload } from "../hooks/useFileUpload";
import { Header } from "../components/Header";
import { FileTable } from "../components/FileTable";
import { AlertTable } from "../components/AlertTable";
import { UploadModal } from "../components/UploadModal";

export default function Page() {
  const { files, isLoading: filesLoading, error: filesError, refetch: refetchFiles } = useFiles();
  const { alerts, isLoading: alertsLoading, error: alertsError } = useAlerts();
  const { isSubmitting, error: uploadError, upload, clearError } = useFileUpload();

  const [showModal, setShowModal] = useState(false);

  const handleUpload = async (title: string, file: File) => {
    await upload(title, file, () => {
      setShowModal(false);
      refetchFiles();
    });
  };

  const errorMessage = filesError || alertsError || uploadError;

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <Header
                onRefresh={refetchFiles}
                onAddFile={() => {
                  clearError();
                  setShowModal(true);
                }}
              />
            </Card.Body>
          </Card>

          {errorMessage ? (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          ) : null}

          <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Файлы</h2>
                <Badge bg="secondary">{files.length}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <FileTable files={files} isLoading={filesLoading} />
            </Card.Body>
          </Card>

          <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Алерты</h2>
                <Badge bg="secondary">{alerts.length}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <AlertTable alerts={alerts} isLoading={alertsLoading} />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <UploadModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onSubmit={handleUpload}
        isSubmitting={isSubmitting}
        error={uploadError}
        clearError={clearError}
      />
    </Container>
  );
}
